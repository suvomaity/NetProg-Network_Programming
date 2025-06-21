#!/usr/bin/env python3

from mininet.net import Mininet
from mininet.topo import SingleSwitchTopo
from mininet.cli import CLI
from mininet.log import info, setLogLevel

setLogLevel("info")
Single = SingleSwitchTopo(k=2)
net = Mininet(topo=Single)
net.start()
CLI(net)
net.stop()
