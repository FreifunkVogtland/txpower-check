Simple TX-Power check
=====================

Nodes running the official b20170319-v (or newer) build report the (raw) txpower
configuration. It is added by ffmap-backend to the nodes.json. This information
can be combined with the offset table from libiwconfig. The resulting data can
be compared again the allowed limits.

txpower-check simplifies the search for misconfigured nodes:

    curl https://mapdata.freifunk-vogtland.net/nodes.json -o nodes.json
    ./txpower-check.py nodes.json

Both commands will be started automaticall when calling

    ./check.sh

The output is a simple list of links to the map and followed by the offending
transmission power settings

    http://vogtland.freifunk.net/map/#!v:m;n:dc9fdb72567d
     * 5.180 GHz:  36.00 dBm (limit  20.00 dBm)
    http://vogtland.freifunk.net/map/#!v:m;n:f4f26dc1faa2
     * 2.462 GHz:  26.00 dBm (limit  20.00 dBm)
