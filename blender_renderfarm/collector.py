"""
Module containing functions to collect rendered frames from the render nodes.
"""
import logging
from json import dumps, loads
from os import rmdir
from os.path import join as pjoin
from tempfile import mkdtemp
from threading import Thread

import requests

from blender_renderfarm.utils import get_info


def render_collector(node, start, end, step, offset, directory):
    for frame in range(start+offset, end+offset, step):
        with open(pjoin(directory, f"{frame}.ppm"), "w") as framefile:
            framefile.write(requests.get(f"http://{node}:8080/images/ppm/{frame}.ppm"))
