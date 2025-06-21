#!/usr/bin/env python3
"""
Create a network where different switches are connected
to different controllers, by creating a custom Switch subclass.
"""

from mininet.net import Mininet
from mininet.node import OVSSwitch, Controller, RemoteController
from mininet.topolib import TreeTopo
from mininet.log import setLogLevel, info
from mininet.cli import CLI

setLogLevel('info')

# Define controllers
c0 = Controller('c0', port=6633)
c1 = Controller('c1', port=6634)
c2 = RemoteController('c2', ip='127.0.0.1', port=6635)  # Use a different port than c0

# Map switches to controllers
cmap = {
    's1': c0,
    's2': c1,
    's3': c2  # Switch 's3' will connect to remote controller c2
}

class MultiSwitch(OVSSwitch):
    """
    Custom Switch subclass that connects to different controllers.
    """
    def start(self, controllers):
        return OVSSwitch.start(self, [cmap[self.name]])

# Create Mininet object
net = Mininet(topo=TreeTopo(depth=2, fanout=2), switch=MultiSwitch, build=False, waitConnected=True)

# Add controllers
for c in [c0, c1, c2]:
    net.addController(c)

# Build and start the network
net.build()
net.start()

CLI(net)
net.stop()
