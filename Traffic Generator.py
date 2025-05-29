
# Traffic Generator (Python)

# File: traffic_generator.py

from mininet.net import Mininet
from mininet.cli import CLI
from mininet.node import RemoteController
from time import sleep
import os

def generate_udp_traffic(net, src='h1', dst='h2', port=5001, duration=10):
    h1 = net.get(src)
    h2 = net.get(dst)

    print("[*] Starting iperf UDP server on h2")
    h2.cmd(f'iperf -s -u -p {port} -D')
    sleep(1)

    print(f"[*] Sending UDP traffic from {src} to {dst} on port {port} for {duration}s")
    h1.cmd(f'iperf -c {h2.IP()} -u -p {port} -t {duration} -b 10M')
    print("[*] Traffic generation complete")

    print("[*] Stopping iperf server")
    h2.cmd('kill %iperf')

def generate_tcp_traffic(net, src='h1', dst='h2', port=5001, duration=10):
    h1 = net.get(src)
    h2 = net.get(dst)

    print("[*] Starting iperf TCP server on h2")
    h2.cmd(f'iperf -s -p {port} -D')
    sleep(1)

    print(f"[*] Sending TCP traffic from {src} to {dst} on port {port} for {duration}s")
    h1.cmd(f'iperf -c {h2.IP()} -p {port} -t {duration}')
    print("[*] Traffic generation complete")

    print("[*] Stopping iperf server")
    h2.cmd('kill %iperf')

def main():
    from topo import create_topology
    from mininet.net import Mininet
    from mininet.node import RemoteController, OVSSwitch
    from mininet.link import TCLink

    topo = create_topology()
    net = Mininet(topo=topo,
                  switch=OVSSwitch,
                  controller=None,
                  autoSetMacs=True,
                  link=TCLink)

    c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6653)
    net.start()

    generate_tcp_traffic(net, duration=5)
    generate_udp_traffic(net, duration=5)

    CLI(net)
    net.stop()

if __name__ == '__main__':
    main()
