# File: traffic_test_palb.py

from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel
from topo_palb import LoadBalancerTopo
from time import sleep


def run_traffic(net):
    h1 = net.get('h1')
    servers = [net.get(f'h{i}') for i in range(2, 6)]

    print("[*] Starting iperf servers on backend hosts")
    for server in servers:
        server.cmd('iperf -s -p 5001 -D')
    sleep(1)

    print("[*] Generating traffic from h1 to all servers through load balancer")
    for i in range(4):
        h1.cmd(f'iperf -c 10.0.0.{i + 2} -p 5001 -t 2')
        sleep(1)

    print("[*] Traffic generation complete. Stopping iperf servers")
    for server in servers:
        server.cmd('kill %iperf')


def main():
    topo = LoadBalancerTopo()
    net = Mininet(topo=topo,
                  switch=OVSSwitch,
                  controller=None,
                  autoSetMacs=True,
                  link=TCLink)

    c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6653)
    net.start()

    run_traffic(net)
    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    main()
