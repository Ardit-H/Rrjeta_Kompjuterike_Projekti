import socket
import threading
import time

SERVER_IP = "0.0.0.0"
SERVER_PORT = 5555
MAX_CLIENTS = 4
TIMEOUT = 60

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((SERVER_IP, SERVER_PORT))
print(f"Serveri u startua në {SERVER_IP}:{SERVER_PORT}")