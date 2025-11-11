import socket

SERVER_IP = "192.168.1.100"
SERVER_PORT = 5555
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = (SERVER_IP, SERVER_PORT)

print("Klient READ-ONLY u lidh me serverin.")
print("Komandat: /list, /read, /search, exit")

while True:
      msg = input(">> ")
      client.sendto(msg.encode(), server_address)
      data, _ = client.recvfrom(4096)
      print(data.decode())

      if msg == "exit":
         break

      client.close()