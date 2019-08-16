import ffmpeg
from os.path import join as pjoin
from os import listdir

def encode_frames(directory:str, output:str, framerate:int, pad_length:int):
    frames = ffmpeg.input(pjoin(directory, f"%0{pad_length}d.png"), **{"pattern_type": "sequence"})
    frames = ffmpeg.filter(frames, "fps", fps=framerate)
    frames = ffmpeg.output(frames, output)
    frames = ffmpeg.overwrite_output(frames)
    ffmpeg.run(frames)

    