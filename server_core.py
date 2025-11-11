import os
import time
from server_setup import server, clients, lock, MAX_CLIENTS, log_message

def send_message(message, addr):
    server.sendto(message.encode(), addr)

def handle_messages():
    while True:
        data, addr = server.recvfrom(4096)
        msg = data.decode().strip()
        with lock:
            if addr not in clients:
                if len(clients) >= MAX_CLIENTS:
                    send_message("Serveri është plot.", addr)
                    continue

                privilege = "admin" if len(clients) == 0 else "read"
                clients[addr] = {"last_active": time.time(), "messages": 0, "bytes": 0, "privilege": privilege}
                print(f"Klient i ri: {addr} (privilege: {privilege})")

            clients[addr]['last_active'] = time.time()
            clients[addr]['messages'] += 1
            clients[addr]['bytes'] += len(data)

            log_message(addr, msg)