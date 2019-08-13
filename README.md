# Note
This repository depends on functionality within Blender that is buggy, and has been removed from the latest versions of Blender. You might need a modified build of Blender 2.7 or earlier with a patched frameserver that supports non-sequential frame downloads. This patch is out of this project's scope and therefore not included. I'm currently looking for alternative solutions, but until found and implemented, this repository will not receive any further updates or support.

# Blender Renderfarm
Python package for rendering blendfiles with multiple Blender nodes on the network.
Includes a bpy script to be run on the Blender nodes to allow Blender to receive files to render.

## Installation
1. Make sure you're on Py37 (earlier versions of python are untested)
2. Clone the repo.
3. Get [Poetry](https://poetry.eustace.io)
4. Run `poetry install --no-dev`
5. Get [FFmpeg](https://www.ffmpeg.org/)
6. Start your Blender nodes with `blender -P main.py -b` (main.py is located in blender_renderfarm/blender_scripts)

## How to use
After installing the package, you can use `poetry run py -m blender_renderfarm` to run the package. It will ask for the blendfile, and where to save the rendered file, the script will try to do the rest.

## TODO
 - Add a `farmspec` file for specifying where are the Blender nodes (skip the autodiscovery step)
 - Autogenerate a `farmspec` file (if not present) after the first node discovery has been done  

& whatever's in issues at the moment
