#mtd_topo.py
#!/usr/bin/env python3


from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.log import setLogLevel

class MTDTopo(Topo):
    def build(self):
        switch = self.addSwitch('s1')

        host1 = self.addHost('h1', ip='10.0.0.1')
        host2 = self.addHost('h2', ip='10.0.0.2')

        self.addLink(host1, switch)
        self.addLink(host2, switch)

if __name__ == '__main__':
    setLogLevel('info')
    net = Mininet(topo=MTDTopo(), controller=RemoteController)
    net.start()
    CLI(net)
    net.stop()
