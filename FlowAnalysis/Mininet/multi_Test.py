#!/usr/bin/env python3
"""
This example shows how to create a network and run
multiple tests. For a more complicated test example, see udpbwtest.py.
"""

from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.net import Mininet
from mininet.node import OVSKernelSwitch
from mininet.topolib import TreeTopo

def ifconfigTest(net):
    "Run ifconfig on all hosts in the network."
    for host in net.hosts:
        info(f"*** ifconfig for {host.name} ***\n")
        info(host.cmd('ifconfig'))

if __name__ == '__main__':
    setLogLevel('info')  # use setLogLevel instead of lg.setLogLevel
    info("*** Initializing Mininet and kernel modules\n")
    
    OVSKernelSwitch.setup()

    info("*** Creating Tree Topology network\n")
    network = Mininet(
        topo=TreeTopo(depth=2, fanout=2),
        switch=OVSKernelSwitch,
        waitConnected=True
    )

    info("*** Starting network\n")
    network.start()

    info("*** Running ping test\n")
    network.pingAll()

    info("*** Running ifconfig test\n")
    ifconfigTest(network)

    info("*** Starting CLI (type 'exit' to exit)\n")
    CLI(network)

    info("*** Stopping network\n")
    network.stop()
