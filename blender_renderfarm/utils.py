from requests import get, Timeout


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


def info_wrapper(node, results):
    results.append((get_info(node), node))