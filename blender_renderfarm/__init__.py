import requests, socket, ipaddress
__version__ = '0.1.0'


def discover_nodes(node_net=ipaddress.ip_network(socket.gethostbyname(socket.getfqdn()))):
    print(node_net)

if __name__ == "__main__":
    discover_nodes()