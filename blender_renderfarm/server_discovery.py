"""
Module containing functions to discover Blender Frameservers and other utility functions
"""
import ipaddress
import socket
from threading import Thread

from requests import get
from requests.exceptions import Timeout


def check_port(ip:str, results:list, port:int=3558):
    """
    Check if port is open on a given IP, and append the ip to results if it is.  

    :param ip: IP to check  
    :param port: Port to check  
    :param results: Object implementing the `.append` method. 
    Stores IPs that have the given port open.  
    """
    data = b""
    socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(1)
    socket_obj.settimeout(60)
    try:
        socket_obj.connect((ip, port))
        socket_obj.sendall(b"PING")
        data = socket_obj.recv(1024)
        socket_obj.close()
        if data == b"PONG":
            results.append(ip)
    except socket.timeout:
        pass
    except ConnectionError:
        pass


def get_info(node:str):
    """
    Get render info from the node.  

    :param node: Node IP as a string  
    :return: Dict containing gathered info (empty if failed)  
    """
    info = {}
    try:
        data = get(f"http://{node}:8080/info.txt", timeout=1)
    except Timeout:
        return {}
    if data.status_code == 200:
        lines = data.text.strip().split("\n")
        for line in lines:
            pair = line.split(" ")
            info[pair[0]] = int(pair[1])
    return info

def discover_nodes(interface:ipaddress.IPv4Interface=ipaddress.ip_interface(socket.gethostbyname(socket.getfqdn())+"/24")):
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
    checker_threads = [Thread(target=check_port, args=(ip.exploded, nodes)) for ip in ips]
    for thread in checker_threads: thread.start()
    for thread in checker_threads: thread.join()
    return nodes
