import socket

SERVER_IP = "192.168.1.100"
SERVER_PORT = 5555
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = (SERVER_IP, SERVER_PORT)

print("Klient ADMIN u lidh me serverin.")
print("Komandat: /list, /read, /delete, /search, STATS, exit")


