"""
Module containing functions to collect rendered frames from the render nodes.
"""
import requests
from threading import Thread
from tempfile import mkdtemp
from blender_renderfarm.server_discovery import get_info
from json import loads, dumps
from os import rmdir
from os.path import join as pjoin
import logging

def info_wrapper(node, results):
    results.append((get_info(node), node))


def render_collector(node, start, end, step, offset, directory):
    for frame in range(start+offset, end+offset, step):
        with open(pjoin(directory, f"{frame}.ppm"), "w") as framefile:
            framefile.write(requests.get(f"http://{node}:8080/images/ppm/{frame}.ppm"))


def collect_renders(renderers):
    info_collection = []
    logging.info("Creating info collector threads.")
    collector_threads = [Thread(target=info_wrapper, args=(renderer, info_collection)) for renderer in renderers]
    for thread in collector_threads: thread.start()
    logging.info("Threads started. Waiting to finish.")
    for thread in collector_threads: thread.join()
    
    logging.info("Merging nodes based on info sets.")
    info_sets = {} 
    for info, node in info_collection:
        if dumps(info) not in info_sets:
            info_sets[dumps(info)] = [node]
        else:
            info_sets[dumps(info)].append(node)
    
    logging.info("Creating render collector threads.")
    renderer_threads = {}
    tempdirs = []
    for info in info_sets:
        tempdir = mkdtemp()
        renderer_threads[info] = [Thread(target=render_collector, 
            args=(node, 
                  int(loads(info)["start"]), 
                  int(loads(info)["end"]),
                  len(info_sets[info])*int(loads(info)["step"]),
                  info_sets[info].indexof(node),
                  tempdir))
            for node in info_sets[info]]
        for thread in renderer_threads[info]: thread.start()
        tempdirs.append(tempdir)
    
    logging.info("Waiting for renders to finish.")
    for threads in renderer_threads.values():
        for thread in threads: thread.join()
    return tempdir