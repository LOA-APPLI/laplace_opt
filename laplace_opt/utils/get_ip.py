# library
import socket


def get_local_ip() -> str | None:
    '''Return the ip address if founded, else None.'''
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    finally:
        s.close()