import socket
from threading import Thread

def send(node:str, filepath:str, port:int, result:list):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sck:
        sck.connect((node, port))
        with open(filepath, "rb") as blendfile:
            sck.sendall(blendfile.read())


def send_to_nodes(nodes:list, filepath:str, port:int=3558):
    confirmations = []
    threads = [Thread(target=send, args=(node, filepath, port, confirmations)) for node in nodes]
    for thread in threads: thread.start()
    for thread in threads: thread.join()
    return all(confirmations)