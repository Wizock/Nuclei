import logging
from gevent import monkey
from nuclei_backend import app
from gevent.pywsgi import WSGIServer

# add logging for the app

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    monkey.patch_all()
    app.run("0.0.0.0", port=5000, debug=True)
