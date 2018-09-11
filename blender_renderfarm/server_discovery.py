import socket, ipaddress
from threading import Thread
from requests import get

def check_port(ip, port, results):
    """
    Check if port is open on a given IP, and append the ip to results if it is.  

    :param ip: IP to check  
    :param port: Port to check  
    :param results: Object implementing the `.append` method. 
    Stores IPs that have the given port open.  
    """
    socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(1)
    result = socket_obj.connect_ex((ip, port))
    socket_obj.close()
    print(result)
    if result == 0:
        results.append(ip)


def get_info(node):
    """
    Get render info from the node.  

    :param node: Node IP as a string  
    :return: Dict containing gathered info (empty if failed)  
    """
    info = {}
    data = get(f"http://{node}:8080/info.txt")
    if data.status_code == 200:
        lines = data.text.strip().split("\n")
        for line in lines:
            pair = line.split(" ")
            info[pair[0]] = int(pair[1])
    return info

def discover_nodes(interface=ipaddress.ip_interface(socket.gethostbyname(socket.getfqdn())+"/24")):
    """
    Attempts to discover all running Blender Framserver nodes on the local network.  

    :param interface: (Optional) IPvXInterface object containing the IP and subnet
    mask where the nodes can be located.
    :type interface: Union(IPv4Interface, IPv6Interface)
    :return: Returns list of IPvXAddress objects with a currently active Blender Frameserver instance.
    :rtype: list
    """
    ips = interface.network.hosts()
    nodes = []
    checker_threads = [Thread(target=check_port, args=(ip.exploded, 8080, nodes)) for ip in ips]
    for thread in checker_threads: thread.start()
    for thread in checker_threads: thread.join()
    clean_nodes = []
    for node in nodes:
        info = get_info(node)
        if "start" in info and "end" in info:
            clean_nodes.append(node)
    return clean_nodes
