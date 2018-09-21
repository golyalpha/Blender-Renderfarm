"""
Module containing functions to discover Blender Frameservers and other utility functions
"""
import ipaddress
import socket
from typing import Union
from threading import Thread

from requests import get
from requests.exceptions import Timeout
from blender_renderfarm.utils import construct_sck, ping_node


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

def discover_nodes(interface:Union(ipaddress.IPv4Interface,ipaddress.IPv6Interface)=ipaddress.ip_interface(socket.gethostbyname(socket.getfqdn())+"/24")):
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
