import pytest


def test_compress_file():
    # test if compress_file function exists
    import nuclei.compression_service

    assert nuclei.compression_service.compress_file

    # test if compress_file function returns a response
    import nuclei.compression_service

    assert nuclei.compression_service.compress_file() == Response
