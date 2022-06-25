import subprocess

import ffmpeg

from ..extension_globals.celery import celery

"""
transform these functions into generators

yeild the current status

if the status is not 0, then the process failed
if the status is 1, then the process is currently running
and if the status is 2, then the process is finished
else, the process is not running
"""


@celery.task(bind=True)
def compression_low_preset(
    file_path: str, file_path_compressed: str
) -> subprocess.CompletedProcess:
    try:
        result = (
            ffmpeg.input(file_path)
            .output(file_path_compressed, vcodec="libx264", crf=24)
            .run(overwrite_output=True)
        )
    except ffmpeg.Error as e:
        raise e
    except Exception as e:
        raise e
    finally:
        if result.returncode != 0:
            raise Exception("Compression failed")
    return result


@celery.task(bind=True)
def compress_medium_preset(
    file_path: str, file_path_compressed: str
) -> subprocess.CompletedProcess:
    try:
        result = (
            ffmpeg.input(file_path)
            .output(file_path_compressed, vcodec="libx264", crf=28)
            .run(overwrite_output=True)
        )
    except ffmpeg.Error as e:
        raise e
    except Exception as e:
        raise e
    finally:
        if result.returncode != 0:
            raise Exception("Compression failed")
    return result


@celery.task(bind=True)
def compression_high_preset(
    file_path: str, file_path_compressed: str
) -> subprocess.CompletedProcess:
    try:
        result = (
            ffmpeg.input(file_path)
            .output(file_path_compressed, vcodec="libx264", crf=30)
            .run(overwrite_output=True)
        )
    except ffmpeg.Error as e:
        raise e
    except Exception as e:
        raise e
    finally:
        if result.returncode != 0:
            raise Exception("Compression failed")
    return result


@celery.task(bind=True)
def tested_perfect_preset(
    file_path: str, file_path_compressed: str
) -> subprocess.CompletedProcess:
    try:
        result = (
            ffmpeg.input(file_path)
            .output(file_path_compressed, vcodec="libx264", crf=26)
            .run(overwrite_output=True)
        )
    except ffmpeg.Error as e:
        raise e
    except Exception as e:
        raise e
    finally:
        if result.returncode != 0:
            raise Exception("Compression failed")
    return result


@celery.task(bind=True)
def compression_main(
    file_path: str, file_path_compressed: str, preset: str = "perfect"
) -> subprocess.CompletedProcess:
    try:
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
    except ffmpeg.Error as e:
        raise e
    except Exception as e:
        raise e
    finally:
        return
