import subprocess


def compression_low_preset(file_path, file_path_compressed, file):
    return subprocess.run(
        f"ffmpeg -i {file_path}\{file} -vcodec libx264 -crf 24 {file_path_compressed}\{file}",
        shell=True,
    )


def compress_medium_preset(file_path, file_path_compressed, file):
    return subprocess.run(
        f"ffmpeg -i {file_path}\{file} -vcodec libx264 -crf 28 {file_path_compressed}\{file}",
        shell=True,
    )


def compression_high_preset(file_path, file_path_compressed, file):
    return subprocess.run(
        f"ffmpeg -i {file_path}\{file} -vcodec libx264 -crf 30 {file_path_compressed}\{file}",
        shell=True,
    )


def tested_perfect_preset(file_path, file_path_compressed, file):
    return subprocess.run(
        f"ffmpeg -i {file_path}\{file} -vcodec libx264 -crf 26 {file_path_compressed}\{file}",
        shell=True,
    )


def compression_main(file_path, file_path_compressed, file, preset=None):
    if preset == "low":
        compression_low_preset(file_path, file_path_compressed, file)
    elif preset == "medium":
        compress_medium_preset(file_path, file_path_compressed, file)
    elif preset == "high":
        compression_high_preset(file_path, file_path_compressed, file)
    elif preset == "perfect":
        tested_perfect_preset(file_path, file_path_compressed, file)
    else:
        print("No preset selected")
