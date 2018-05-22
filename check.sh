#! /bin/sh

set -e

curl -s https://mapdata.freifunk-vogtland.net/nodes.json -o nodes.json
./txpower-check.py nodes.json
