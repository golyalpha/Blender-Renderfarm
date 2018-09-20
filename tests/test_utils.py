import socket
from blender_renderfarm.utils import get_info

def test_get_info():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_obj:
        socket_obj.bind(("localhost", 8080))
        socket_obj.listen()
        assert get_info("localhost") == {}