from blender_renderfarm.server_discovery import discover_nodes, check_port
import socket

def test_discovery_empty():
    assert discover_nodes() == []

def test_port_check():
    socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_obj.bind(("localhost", 8080))
    nodes = []
    check_port("localhost", 8080, nodes)
    assert all(nodes)