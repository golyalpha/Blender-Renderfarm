import socket
from threading import Thread

from blender_renderfarm.server_discovery import (check_port, discover_nodes,
                                                 get_info)


def test_discovery_empty():
    assert discover_nodes() == []


def test_port_check():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_obj:
        socket_obj.bind(("localhost", 8080))
        socket_obj.listen()
        nodes = []
        check_port("localhost", 8080, nodes)
        assert all(nodes)


def test_get_info():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_obj:
        socket_obj.bind(("localhost", 8080))
        socket_obj.listen()
#        socket_thread = Thread(target=helper_thread, args=(socket_obj,))
#        socket_thread.start()
        assert get_info("localhost") == {}
