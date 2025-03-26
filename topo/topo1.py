from mininet.node import RemoteController, OVSSwitch
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.cli import CLI

class BottleneckTopo(Topo):
    def build(self):
        print("Building topology...")

        # Add hosts (H1 is now the server)
        h1 = self.addHost('h1')  # Server
        h2 = self.addHost('h2')  # Client 1
        h3 = self.addHost('h3')  # Client 2
        print("Added hosts: h1 (Server), h2, h3 (Clients)")

        # Add switches (Core and Distribution layers)
        s1 = self.addSwitch('s1')  # Distribution switch
        s2 = self.addSwitch('s2')  # Distribution switch
        s3 = self.addSwitch('s3')  # Core switch (Bottleneck)
        print("Added switches: s1, s2 (Distribution), s3 (Core)")

        # Connect hosts to distribution switches
        self.addLink(h1, s1)  # Server to Switch 1
        self.addLink(h2, s2)  # Client 1 to Switch 2
        self.addLink(h3, s2)  # Client 2 to Switch 2
        print("Connected hosts to switches.")

        # Connect distribution switches to core switch (S3)
        self.addLink(s1, s3, bw=1, loss=5, delay='20ms')  # Bottleneck link
        self.addLink(s2, s3, bw=1, loss=5, delay='20ms')
        print("Connected distribution switches to core switch with bottlenecks.")

if __name__ == '__main__':
    print("Starting Mininet network...")
    topo = BottleneckTopo()

    try:
        net = Mininet(topo=topo, controller=RemoteController('c0', ip='127.0.0.1', port=6633), 
                      switch=OVSSwitch, link=TCLink)
        print("Mininet network created successfully.")

        # Enable Internet access
        net.addNAT().configDefault()

        print("Starting the network...")
        net.start()

        # Start the server on H1
        print("Starting iPerf3 Server on H1...")
        server = net.get('h1')
        server.cmd("iperf3 -s -D")  # Run iPerf3 server in the background

        print("Network is ready. Use the CLI for testing.")
        CLI(net)

    except Exception as e:
        print(f"Error starting the network: {e}")
        exit(1)

    print("Stopping the network...")
    net.stop()
    print("Network stopped successfully.")

