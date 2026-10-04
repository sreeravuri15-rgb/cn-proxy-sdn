from mininet.net import Mininet
from mininet.node import OVSSwitch, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel


def create_topology():
    net = Mininet(
        controller=RemoteController,
        switch=OVSSwitch
    )

    print("*** Adding controller")
    c0 = net.addController(
    "c0",
    controller=RemoteController,
    ip="127.0.0.1",
    port=6653
)

    print("*** Adding hosts")
    client1 = net.addHost("client1")
    client2 = net.addHost("client2")
    proxy = net.addHost("proxy")
    server = net.addHost("server")

    print("*** Adding switch")
    s1 = net.addSwitch("s1")

    print("*** Creating links")
    net.addLink(client1, s1)
    net.addLink(client2, s1)
    net.addLink(proxy, s1)
    net.addLink(server, s1)

    print("*** Starting network")
    net.start()

    print("*** Network started")
    CLI(net)

    print("*** Stopping network")
    net.stop()


if __name__ == "__main__":
    setLogLevel("info")
    create_topology()
