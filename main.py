import socket
import sys
import logging as log

from server import ChatServer

log.basicConfig(stream=sys.stdout, level=log.DEBUG)


def bind_socket(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
    except Exception as e:
        log.critical(e)
        sys.exit(1)
    return sock


if __name__ == '__main__':
    server = ChatServer()
    log.info('Created a server')

    host = ''
    port = 2222
    if len(sys.argv) == 2:
        host = sys.argv[1]
        port = sys.argv[2]
    sock = bind_socket(host, port)

    log.info('Listening for connections')
    while True:
        sock.listen(10)
