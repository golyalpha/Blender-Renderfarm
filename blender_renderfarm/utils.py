from requests import get, Timeout
import socket

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


def info_wrapper(node:str, results:list):
    """
    Multithreading wrapper for the get_info function.
    Appends the retval of get_info to the results object.
    """
    results.append((get_info(node), node))


def construct_sck():
    """
    Utility function.
    Constructs socket with 60sec timeout and returns it.
    """
    socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_obj.settimeout(60)
    return socket_obj


def ping_node(ip:str, port:int, socket_obj:socket.socket):
    """
    Utility function.
    Sends ping to a render node's socket.
    """
    data = b""
    socket_obj.connect((ip, port))
    socket_obj.sendall(b"PING")
    data = socket_obj.recv(1024)
    socket_obj.close()
    return data == b"PONG"