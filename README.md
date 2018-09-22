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
After installing the package, you can use `poetry run py blender_renderfarm` to run the package. It will ask for the blendfile, and where to save the rendered file, the script will try to do the rest.

## TODO
 - Add a `farmspec` file for specifying where are the Blender nodes (skip the autodiscovery step)
 - Autogenerate a `farmspec` file (if not present) after the first node discovery has been done
