import socket, ipaddress
from threading import Thread
from requests import get

def check_port(ip, port, results):
    socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(1)
    result = socket_obj.connect_ex((ip, port))
    socket_obj.close()
    results.append(ip if result == 0 else False)


def discover_nodes(interface=ipaddress.ip_interface(socket.gethostbyname(socket.getfqdn())+"/24")):
    ips = interface.network.hosts()
    nodes = []
    threads = [Thread(target=check_port, args=(ip.exploded, 8080, nodes)) for ip in ips]
    for thread in threads: thread.start()
    for thread in threads: thread.join()
    nodes = [node for node in nodes if node]
    clean_nodes = []
    for node in nodes:
        data = get(f"http://{node}:8080/info.txt")
        if data.status_code == 200:
            lines = data.text.strip().split("\n")
            info = {}
            for line in lines:
                pair = line.split(" ")
                info[pair[0]] = int(pair[1])
            if "start" in info and "end" in info:
                clean_nodes.append(node)
    return clean_nodes
    


if __name__ == "__main__":
    print("Discovering running Blender FrameServer nodes.")
    print(discover_nodes())