"""
Module containing functions to collect rendered frames from the render nodes.
"""
import logging
from json import dumps, loads
from os import rmdir
from os.path import join as pjoin
from threading import Thread
import requests

from .utils import get_info


def frame_collector(node:str, start:int, end:int, step:int, offset:int, directory:str):
    for frame in range(start+offset, end+1, step):
        print("Collecting frame", frame)
        with open(pjoin(directory, f"{frame:0{len(str(end))}}.png"), "wb") as framefile:
            framefile.write(requests.get(f"http://{node}:8080/image/{frame:0{len(str(end))}}.png").content)
    try:
        requests.get(f"http://{node}:8080/close.txt", timeout=10)
        print("Frames from", node, "collected.")
    except ConnectionError:
        pass


def collect_frames(nodes:list, directory:str):
    render_info = get_info(nodes[0])
    threads = [Thread(target=frame_collector, args=(
        node, 
        render_info["start"],
        render_info["end"],
        len(nodes),
        nodes.index(node),
        directory)) for node in set(nodes)]
    for thread in threads: thread.start()
    for thread in threads: thread.join()