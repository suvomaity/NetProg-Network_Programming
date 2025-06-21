#!/usr/bin/env python3

from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.node import OVSController, OVSSwitch

def create_minimal_topo():
    "Creates an empty network and adds nodes to it"
    
    info('*** Creating Network\n')
    net = Mininet(controller=OVSController)

    info('*** Adding Controller\n')
    net.addController(name='c0')

    info('*** Adding Hosts\n')
    h1 = net.addHost(name='h1', ip='20.0.0.1/24')
    h2 = net.addHost(name='h2', ip='20.0.0.2/24')
    info(f'{h1.name}, {h2.name}\n')

    info('*** Adding Switch\n')
    s1 = net.addSwitch(name='s1', cls=OVSSwitch)
    info(f'{s1.name}\n')

    info('*** Creating Links\n')
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    info('(h1 <-> s1)\n(h2 <-> s1)\n')

    info('*** Starting Network\n')
    net.start()

    info('*** Running CLI\n')
    CLI(net)

    info('*** Stopping Network\n')
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    create_minimal_topo()
