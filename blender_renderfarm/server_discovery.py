"""
Module containing functions to discover Blender Frameservers and other utility functions
"""
import ipaddress
import socket
from threading import Thread

from requests import get
from requests.exceptions import Timeout
from time import time
from .utils import construct_sck, ping_node


def check_port(ip:str, results:list, port:int=3558):
    """
    Check if port is open on a given IP, and append the ip to results if it is.  

    :param ip: IP to check  
    :param port: Port to check  
    :param results: Object implementing the `.append` method. 
    Stores IPs that have the given port open.  
    """
    try:
        if ping_node(ip, port, construct_sck()):
            results.append(ip)
    except socket.timeout:
        pass
    except ConnectionError:
        pass

def discover_nodes():
    """
    Attempts to discover all running Blender Framserver nodes on the local network.  

    :return: List of IPs of active nodes.
    :rtype: list
    """
    nodes = []
    sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sck.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sck.bind(("", 3558))
    sck.settimeout(10)
    now = time()
    while time()-now < 10:
        data, addr = sck.recvfrom(1024)
        if data == b"BR_NOTIFY" and addr[0] not in nodes:
            print("Discovered new node:", addr[0])
            nodes.append(addr[0])
            now = time()
    return nodes
