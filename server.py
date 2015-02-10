import threading

import paramiko


class Server(paramiko.ServerInterface):

    def __init__(self, ):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session' or kind == 'shell':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def get_allowed_auths(self, username):
        return 'publickey'

    def check_auth_password(self, username, password):
        return paramiko.AUTH_SUCCESSFUL


    def check_auth_publickey(self, username, key):
        return True

    def check_channel_shell_request(self, channel):
        return True
