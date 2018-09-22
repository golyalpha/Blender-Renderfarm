from server_discovery import discover_nodes
from send_blend import send_to_nodes
from collector import collect_frames
from encoder import encode_frames
from utils import get_info
from tempfile import TemporaryDirectory
from tkinter import filedialog
from tkinter import Tk

Tk().withdraw()

blendfile = filedialog.askopenfilename()
outfile = filedialog.asksaveasfilename()

print("Discovering nodes.")
nodes = discover_nodes()
print("Found:")
for node in nodes: print(node)
print()
print("Sending blendfile to nodes.")
send_to_nodes(nodes, blendfile)
info = get_info(nodes[0])
with TemporaryDirectory() as renderDir:
    print("Collecting frames.")
    collect_frames(nodes, renderDir)
    print("Encoding frames.")
    encode_frames(renderDir, outfile, info["rate"])
    print("Done!")