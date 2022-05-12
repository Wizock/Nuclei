import subprocess


def compression_low_preset():
    low_preset = subprocess.run(
        "ffmpeg -i input.mp4 -vcodec libx264 -crf 24 low_output.mp4",
        shell=True,
    )


def compress_medium_preset():
    medium_preset = subprocess.run(
        "ffmpeg -i input.mp4 -vcodec libx264 -crf 28 medium_output.mp4",
        shell=True,
    )


def compression_high_preset():
    medium_preset = subprocess.run(
        "ffmpeg -i input.mp4 -vcodec libx264 -crf 30 high_output.mp4",
        shell=True,
    )


def tested_perfect_preset():
    perfect_prest = subprocess.run(
        "ffmpeg -i input.mp4 -vcodec libx264 -crf 26 perfect_output.mp4", shell=True
    )


if __name__ == "__main__":
    compression_low_preset()
    compress_medium_preset()
    compression_high_preset()
    tested_perfect_preset()
