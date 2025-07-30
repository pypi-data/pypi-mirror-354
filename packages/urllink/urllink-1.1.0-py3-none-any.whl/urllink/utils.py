import socket

def check_internet(host="8.8.8.8", port=53, timeout=3):
    """
    Checks if internet connection is available.
    """
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error:
        return False
