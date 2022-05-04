from nuclei import Nuclei


# create socket_register class
class Socket_Register(object):
    def __init__(self, app: Nuclei):
        self.app = app

    def register_socket(self):
        from nuclei.compression_service.socket import compression_service_socket

        self.app.socketio.on_namespace(compression_service_socket(self.app))

    def register_socket_events(self):
        from nuclei.compression_service.socket import compression_service_socket_events

        self.app.socketio.on_namespace(compression_service_socket_events(self.app))
