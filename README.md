# Note
~~This repository depends on functionality within Blender that is buggy, and has been removed from the latest versions of Blender. You might need a modified build of Blender 2.7 or earlier with a patched frameserver that supports non-sequential frame requests. This patch is out of this project's scope and therefore not included. I'm currently looking for alternative solutions, but until found and implemented, this repository will not receive any further updates or support.~~

The above is no longer true, as a suitable replacement for the frameserver has now been included with the blender script. Please note that this no longer follows the standard Frameserver specification and serves PNGs, instead of PPM files.
This project has however been unmaintained since Blender 2.7, and therefore is likely to not work in Blender 2.8 or newer. I've lost any reason to further maintain this, as I started using Kubernetes, which can achieve the same goal using a batch Job, without needing to run any non-project scripts in Blender. 

Here's a high level overview of how that can be done:  
Use a shared volume for renders and tell Blender use placeholders and not overwrite render results. Each instance of blender will now create an empty file when it starts rendering, and skipping the frames that already have a corresponding file created, leading to the most efficient scheduling in environments where each node renders at different speeds, or frame complexity varies from frame to frame.
Now all you need to do, is have a job run FFMPEG on the frame files to encode them into a video sequence, and maybe startup another instance of Blender to mixdown the audio from your project so you can make the full result with both audio and video.

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
