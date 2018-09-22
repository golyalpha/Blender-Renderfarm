# Blender Renderfarm
Python package for rendering blendfiles with multiple Blender nodes on the network.
Includes a bpy script to be run on the Blender nodes to allow Blender to receive files to render.

## Installation
1. Clone the repo.
2. Get [Poetry](https://poetry.eustace.io)
3. Run `poetry install --no-dev`
4. Get [FFmpeg](https://www.ffmpeg.org/)
4. Start your Blender nodes with `blender -P main.py -b` (main.py is located in blender_renderfarm/blender_scripts)

## How to use
After installing the package, you can use `poetry run py blender_renderfarm` to run the package. It will ask for the blendfile, and where to save the rendered file, the script will try to do the rest.

## TODO
 - Add a `farmspec` file for specifying where are the Blender nodes (skip the autodiscovery step)
