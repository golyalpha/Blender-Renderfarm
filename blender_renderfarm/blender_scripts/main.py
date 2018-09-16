import bpy
import os
from bpy.app.handlers import persistent
import socket
from tempfile import NamedTemporaryFile


@persistent
def handle_render():
    print("Render finished, waiting for a new file.")    
    with NamedTemporaryFile(delete=False, suffix=".blend") as datafile:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("0.0.0.0", 3558))
            s.listen(0)
            conn, addr = s.accept()
            with conn:
                print("Receiving blend file from {}".format(addr))
                while True:
                    data = conn.recv(1024)
                    if not data: break
                    datafile.write(data)
    bpy.ops.wm.open_mainfile(filepath=datafile.name)
    bpy.data.scenes['Scene'].render.image_settings.file_format = 'FRAMESERVER'
    bpy.ops.render.render(animation=True)
    os.remove(datafile.name)

bpy.app.handlers.render_complete.append(handle_render)
handle_render()