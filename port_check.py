import socket

def check_port(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    return result == 0

open_ports = [port for port in range(1, 65536) if check_port(port)]

print("Open ports:", open_ports)
