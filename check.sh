#! /bin/sh

set -e

curl -s https://vpn01.freifunk-vogtland.net/ffv/nodes.json -o nodes.json
./txpower-check.py nodes.json
