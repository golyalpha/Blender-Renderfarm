import requests
from threading import Thread
from tempfile import TemporaryDirectory
from server_discovery import get_info


def info_wrapper(node, results):
    results.append((get_info(node), node))

def collect_renders(renderers):
    info_collection = []
    collector_threads = [Thread(target=info_wrapper, args=(renderer, info_collection)) for renderer in renderers]
    for thread in collector_threads: thread.start()
    for thread in collector_threads: thread.join()
    
    info_sets = {} 
    for info, node in info_collection:
        if str(info) not in info_sets:
            info_sets[str(info)] = [node]
        else:
            info_sets[str(info)].append(node)
    print(info_sets.keys())