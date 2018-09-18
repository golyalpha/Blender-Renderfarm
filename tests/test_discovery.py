import socket
import os, signal
from threading import Thread
from blender_renderfarm.server_discovery import (
    check_port, 
    discover_nodes,
    get_info
)
from subprocess import Popen, run
from time import sleep

def test_discovery_empty():
    assert discover_nodes() == []


def test_discovery_filled():
    if run("blender --help", capture_output=True):
        blender = Popen(["blender", "-P", "tests/resources/scripts/main.py", "-b"])
        # TODO: Figure out a more intelligent way to wait for Blender to load.
        sleep(30)
        assert discover_nodes() != []
        # TODO: Figure out a mulit-platform way to force-kill Blender
        print("Don't forget to kill blender")


def test_get_info():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_obj:
        socket_obj.bind(("localhost", 8080))
        socket_obj.listen()
        assert get_info("localhost") == {}
