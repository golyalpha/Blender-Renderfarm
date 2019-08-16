import socket
from threading import Thread
from udp_filetransfer import send


def send_to_nodes(nodes:list, filepath:str):
    return send(filepath)