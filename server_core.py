import os

def send_message(message, addr):
    server.sendto(message.encode(), addr)

def handle_messages():
    while True:
        data, addr = server.recvfrom(4096)
        msg = data.decode().strip()