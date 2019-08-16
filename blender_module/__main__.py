import os
import socket
from shutil import rmtree
from tempfile import mkdtemp
from time import sleep
from threading import Thread
from http.server import BaseHTTPRequestHandler, HTTPServer
import bpy
from bpy.app.handlers import persistent
            

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/info.txt":
            data = {
                "rate": bpy.data.scenes['Scene'].render.fps,
                "start": bpy.data.scenes['Scene'].frame_start,
                "end": bpy.data.scenes['Scene'].frame_end
            }
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            for key, value in data.items():
                self.wfile.write(bytes(f"{key} {value}\n", "UTF-8"))
            return
        if self.path == "/close.txt":
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(bytes("Server stopping now...", "UTF-8"))
            Thread(target=self.server.shutdown).start()
            return
        if self.path.startswith("/image/") and os.path.split(self.path)[1].lower().endswith(".png"):
            image = os.path.split(self.path)[1]
            frame = int(image.split(".")[0])
            outpath = os.path.split(bpy.data.scenes['Scene'].render.filepath)[0]
            bpy.data.scenes['Scene'].frame_set(frame)
            bpy.ops.render.render(write_still=True)
            self.send_response(200)
            self.send_header("Content-Type", "image/png")
            self.end_headers()
            with open(os.path.join(outpath, "currentframe.png"), "rb") as imagefile:
                self.wfile.write(imagefile.read())
            return
        self.send_response(404)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(b"That... doesn't exists tho...")

class Notifier():
    def __init__(self):
        self.sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sck.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self._thread = None
    
    def start(self):
        self.active = True
        self._thread = Thread(target=self._run)
        self._thread.start()
    
    def stop(self):
        self.active = False
        if self._thread is not None:
            self._thread.join()
            self._thread = None
    
    def _run(self):
        while self.active:
            self.sck.sendto(b"BR_NOTIFY", ("<broadcast>", 3558))
            sleep(3)
    
    def close(self):
        self.active = False
        self._thread.join()
        self.sck.close()


@persistent
def handle_render():
    print("Bootstrapping node.")
    try:
        from subprocess import Popen, PIPE
        from bpy.app import binary_path_python as executable
        with Popen([executable, "-m", "pip", "install", "-U", "udp-filetransfer"],
            stdout=PIPE, stderr=PIPE, bufsize=1, universal_newlines=True) as pip:
            pip.communicate()
        import udp_filetransfer
    except ImportError:
        print("Missing a key package. Installing from pip...")
        from itertools import zip_longest
        print("Using", executable, "to install udp-filetransfer.")
        with Popen([executable, "-m", "ensurepip"],
            stdout=PIPE, stderr=PIPE, bufsize=1, universal_newlines=True) as ensurepip:
            ensurepip.communicate()
        with Popen([executable, "-m", "pip", "install", "udp-filetransfer"],
            stdout=PIPE, stderr=PIPE, bufsize=1, universal_newlines=True) as pip:
            pip.communicate()
        if pip.returncode == 0:
            import udp_filetransfer
        else:
            print("Dependencies failed to install. Try running with admin rights.")
            bpy.ops.wm.quit_blender()
            return
        del executable
        del Popen
        del PIPE
        del ensurepip
        del pip
        del zip_longest
    
    print("udp-filetransfer version", udp_filetransfer.__version__)
    print("Bootstrap finished. Awaiting work.")
    notifier = Notifier()
    while True:
        notifier.start()
        datafile = udp_filetransfer.receive(True)
        notifier.stop()
        print(datafile)
        print("Datafile received. Processing...")
        if datafile.endswith(".zip"):
            target_dir = mkdtemp()
            from zipfile import ZipFile
            with ZipFile(datafile) as pack:
                pack.extractall(target_dir)
            for root, dirs, files in os.walk(target_dir):
                for f in files:
                    if f.endswith(".blend"):
                        datafile = os.path.join(root, f)
                        break
                if datafile.endswith(".blend"):
                    break
        outdir = mkdtemp()
        print("Datafile processed. Preparing for render...")
        bpy.ops.wm.open_mainfile(filepath=datafile)
        bpy.data.scenes['Scene'].render.image_settings.file_format = 'PNG'
        endframe = bpy.data.scenes['Scene'].frame_end
        bpy.data.scenes['Scene'].render.filepath = os.path.join(
            outdir,
            "currentframe.png"
        )
        print("Render ready.")
        with HTTPServer(("", 8080), Handler) as httpd:
            print("Starting frameserver...")
            httpd.serve_forever(1)
        rmtree(outdir)
        try:
            rmtree(target_dir)
        except UnboundLocalError:
            pass
        os.remove(datafile)
        print("Render finished, waiting for a new file.")  

handle_render()
