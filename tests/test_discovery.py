import socket
import os, signal
from threading import Thread
from blender_renderfarm.server_discovery import (
    check_port, 
    discover_nodes
)
from subprocess import Popen, run
from time import sleep

def test_discovery_empty():
    assert discover_nodes() == []


def test_discovery_running():
    if run("blender --help", capture_output=True):
        blender = Popen(["blender", "-P", "tests/resources/scripts/main.py", "-b"])
        # TODO: Figure out a more intelligent way to wait for Blender to load.
        sleep(30)
        nodes = discover_nodes()
        assert nodes != []
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sck:
            sck.connect(("localhost", 3558))
            sck.sendall(b"STOP")
            if sck.recv(1024) != b"ACK":
                raise Exception("Blender failed to respond properly.")
