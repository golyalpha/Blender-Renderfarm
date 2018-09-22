import ffmpeg
from os.path import join as pjoin
from os import listdir

def encode_frames(directory:str, output:str, framerate:int):
    frames = ffmpeg.input(pjoin(directory, "%03d.ppm"), **{"pattern_type": "sequence"})
    frames = ffmpeg.filter(frames, "fps", fps=framerate)
    frames = ffmpeg.output(frames, output)
    frames = ffmpeg.overwrite_output(frames)
    ffmpeg.run(frames)

    