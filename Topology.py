
# Mininet topology file (Python)

# File: topo.py

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel

def create_topology():
    topo = Topo()

    # Add a single switch
    s1 = topo.addSwitch('s1')

    # Add hosts
    h1 = topo.addHost('h1', ip='10.0.0.1/24')
    h2 = topo.addHost('h2', ip='10.0.0.2/24')

    # Create links
    topo.addLink(h1, s1, bw=10)
    topo.addLink(h2, s1, bw=10)

    return topo

def run():
    topo = create_topology()
    net = Mininet(topo=topo,
                  switch=OVSSwitch,
                  controller=None,
                  autoSetMacs=True,
                  link=TCLink)

    # Add remote controller
    c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6653)

    net.start()
    print("\n*** Network started. Hosts: h1 <--> s1 <--> h2")
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
