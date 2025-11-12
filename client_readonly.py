import socket
import time

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5555

def readonly_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (SERVER_IP, SERVER_PORT)

    try:
        client.sendto("ping".encode(), server_address)
        client.settimeout(5)
        data, _ = client.recvfrom(4096)
        client.settimeout(None)
    except:
        print("Nuk mund të lidhem me serverin!")
        return

    print("Klient READ-ONLY u lidh me serverin.")
    print("Komandat: /list, /read, /search <keyword>, /info <file>, STATS, exit")
    print("-" * 50)


