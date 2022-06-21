import os
from .main import storage_sequencer_controller
import logging
import ipfshttpclient

from flask import Response, request, send_file
import requests


def _download(url: str) -> Response:
    _headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br, identity",
        "Connection": "keep-alive",
    }
    _get_request = requests.get(url, stream=True, headers=_headers, verify=False)
    try:
        _get_request.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logging.error(f"error: {e}")
        return e
    if _get_request.headers.get("content-type") == "application/octet-stream":
        return send_file(_get_request.raw, attachment_filename=url.split("/")[-1])


@storage_sequencer_controller.route("/<path:path>")
@storage_sequencer_controller.route("/download/<path:path>")
def download(path: str):
    try:
        _path = os.path.splittext(path)[0]
        _hash = str(_path[0])

        if not _hash or not _hash.startswith("Qm"):
            return Response(
                f"Invalid hash: {_hash}",
                status=400,
            )
        logging.info(
            f"_hash: {_hash}",
        )

        url = storage_sequencer_controller.config["IPFS_CONNECT_URL"] + "/" + _hash

        return download(url)
    except Exception as e:
        logging.error(f"error: {e}")
        return e, 503
