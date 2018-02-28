#!/usr/bin/python3
# -*- coding: utf-8; -*-

import json
import os
import os.path
import sys

# taken from gluon 2016.2.4 libiwinfo hardware.txt
model_offsets = {
    "Ubiquiti PicoStation2 HP":     1000,
    "Ubiquiti LiteStation2":        1000,
    "Ubiquiti LiteStation5":         500,
    "Ubiquiti NanoStation2":        1000,
    "Ubiquiti NanoStation5":         500,
    "Ubiquiti NanoStation Loco2":   1000,
    "Ubiquiti NanoStation Loco5":    500,
    "Ubiquiti Bullet2":             1000,
    "Ubiquiti Bullet5":              500,
    "Ubiquiti PicoStation M2":      1200,
    "Ubiquiti NanoStation M2":      1100,
    "Ubiquiti NanoStation Loco M2":  800,
    "Ubiquiti NanoStation M5":      1600,
    "Ubiquiti Bullet M2":           1200,
    "Ubiquiti Bullet M5":            500,
}


def get_name(nodes, node_id):
    for n in nodes['nodes']:
        if 'nodeinfo' not in n:
            continue

        if 'node_id' not in n['nodeinfo']:
            continue

        if node_id != n['nodeinfo']['node_id']:
            continue

        if 'hostname' not in n['nodeinfo']:
            continue

        return n['nodeinfo']['hostname']

    return None


# WARNING this is not actually 100% correct because it depends also on
# configured channel width
#
# from see wireless-regdb.git/tree/db.txt?h=master-2017-03-07
def get_regdb(frequency):
    if frequency >= 2400 and frequency <= 2483.5:
        return 2000

    if frequency >= 5150 and frequency <= 5250:
        return 2000

    if frequency >= 5250 and frequency <= 5350:
        return 2000

    if frequency >= 5470 and frequency <= 5725:
        return 2700

    if frequency >= 5725 and frequency <= 5875:
        return 1400

    if frequency >= 57000 and frequency <= 66000:
        return 4000

    return None


def get_limits(model, txpowers):
    offset = 0
    if model in model_offsets:
        offset = model_offsets[model]

    limits = []
    for power in txpowers:
        if 'frequency' not in power:
            continue

        if 'mbm' not in power:
            continue

        regdb = get_regdb(power['frequency'])
        if not regdb:
            continue

        limit = {
            'frequency': power['frequency'],
            'mbm': power['mbm'] + offset,
            'regdb': regdb,
        }

        # skip nodes which have a correct txpower limit
        if limit['mbm'] <= limit['regdb']:
            continue

        limits.append(limit)

    return limits


def print_limits(node_limits, nodes):
    for node_id, data in node_limits.items():
        name = get_name(nodes, node_id)
        if name:
            print(" * %s" % name)

        print("   - http://vogtland.freifunk.net/map/#!v:m;n:%s" % node_id)

        for limit in data:

            cur = limit['mbm']
            freq = limit['frequency']
            regdb = limit['regdb']
            print("   - %u.%03u GHz: %3u.%02u dBm (limit %3u.%02u dBm)" % (
                  int(freq / 1000), int(freq % 1000),
                  int(cur / 100), int(cur % 100),
                  int(regdb / 100), int(regdb % 100)))


def main():
    if len(sys.argv) != 2:
        print("./txpower-check.py nodes.json")
        sys.exit(1)

    nodes_in = sys.argv[1]

    # load
    nodes = json.load(open(nodes_in))

    node_limits = {}
    for n in nodes['nodes']:
        if 'statistics' not in n:
            continue

        if 'txpower' not in n['statistics']:
            continue

        if 'nodeinfo' not in n:
            continue

        if 'node_id' not in n['nodeinfo']:
            continue

        if 'hardware' not in n['nodeinfo']:
            continue

        if 'model' not in n['nodeinfo']['hardware']:
            continue

        node_id = n['nodeinfo']['node_id']
        txpowers = n['statistics']['txpower']
        model = n['nodeinfo']['hardware']['model']

        limits = get_limits(model, txpowers)
        if limits:
            node_limits[node_id] = limits

    print_limits(node_limits, nodes)


if __name__ == "__main__":
    main()
