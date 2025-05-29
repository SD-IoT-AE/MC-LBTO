# File: topo_palb.py

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel

class LoadBalancerTopo(Topo):
    def build(self):
        # Add switch
        lb_switch = self.addSwitch('s1')

        # Add one client
        client = self.addHost('h1', ip='10.0.0.1/24')
        self.addLink(client, lb_switch, bw=10)

        # Add backend servers
        for i in range(2, 6):  # Creates h2 to h5 (4 servers)
            server = self.addHost(f'h{i}', ip=f'10.0.0.{i}/24')
            self.addLink(server, lb_switch, bw=10)

def run():
    topo = LoadBalancerTopo()
    net = Mininet(topo=topo,
                  switch=OVSSwitch,
                  controller=None,
                  autoSetMacs=True,
                  link=TCLink)

    c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6653)
    net.start()

    print("\n[*] Topology started. Client: h1 → Load Balancer: s1 → Servers: h2-h5")
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
