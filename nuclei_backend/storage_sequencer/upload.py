from .main import storage_sequencer_controller
import logging
import ipfshttpclient

from flask import Response, request


@storage_sequencer_controller.route("/upload", methods=["POST", "PUT"])
def upload():
    try:
        # file list
        if "file" in request.files.getlist("file"):
            file_list = request.files.getlist("file")
            logging.info(f"file_list: {file_list}")
            if "IPFS_API_URL" in storage_sequencer_controller.config:
                url = storage_sequencer_controller.config["IPFS_API_URL"] + "/add"
                response = upload(url, file_list)
            client = ipfshttpclient.connect(
                storage_sequencer_controller.config["IPFS_CONNECT_URL"]
            )
            response = client.add(file_list)
        print(f"response: {response}")
        url = (
            storage_sequencer_controller.config["IPFS_CONNECT_URL"]
            + "/"
            + response[0]["Hash"]
        )
        return url
    except Exception as e:
        logging.error(f"error: {e}")
        return e
