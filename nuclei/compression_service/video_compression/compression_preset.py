import subprocess
import ffmpeg
"""
transform these functions into generators

yeild the current status

if the status is not 0, then the process failed
if the status is 1, then the process is currently running
and if the status is 2, then the process is finished
else, the process is not running

"""

@jit(target ="cuda") 
def compression_low_preset(file_path, file_path_compressed):
    return subprocess.run(
        f"ffmpeg -i {file_path} -vcodec libx264 -crf 24 {file_path_compressed}",
        shell=True,
    )

@jit(target ="cuda") 
def compress_medium_preset(file_path, file_path_compressed):
    return subprocess.run(
        f"ffmpeg -i {file_path} -vcodec libx264 -crf 28 {file_path_compressed}",
        shell=True,
    )

def compression_high_preset(file_path, file_path_compressed):
    return subprocess.run(
        f"ffmpeg -i {file_path} -vcodec libx264 -crf 30 {file_path_compressed}",
        shell=True,
    )


def tested_perfect_preset(file_path, file_path_compressed):
    result = (
        ffmpeg.input(file_path)
        .output(file_path_compressed, vcodec="libx264", crf=26)
        .run(overwrite_output=True)
    )
    return result

def compression_main(file_path, file_path_compressed, preset=None):
    if preset == "low":
        compression_low_preset(file_path, file_path_compressed)
    elif preset == "medium":
        compress_medium_preset(file_path, file_path_compressed)
    elif preset == "high":
        compression_high_preset(file_path, file_path_compressed)
    elif preset == "perfect":
        tested_perfect_preset(file_path, file_path_compressed)
    else:
        print("No preset selected")
