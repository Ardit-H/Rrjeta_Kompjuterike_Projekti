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
            if msg.startswith("/list"):
                files = os.listdir(".")
                send_message("\n".join(files), addr)

            elif msg.startswith("/read"):
                parts = msg.split(" ", 1)
                if len(parts) < 2:
                    send_message("Përdorimi: /read <filename>", addr)
                    continue
                filename = parts[1]
                if not os.path.exists(filename):
                    send_message("File nuk ekziston.", addr)
                    continue
                with open(filename, "r", errors="ignore") as f:
                    content = f.read(300)
                send_message(f"Përmbajtja e {filename}:\n{content}", addr)
            elif msg.startswith("/delete"):
                if clients[addr]['privilege'] != "admin":
                    send_message("Nuk ke privilegje për këtë komandë.", addr)
                    continue

                filename = msg.split(" ", 1)[1]
                if os.path.exists(filename):
                    os.remove(filename)
                    send_message(f"File '{filename}' u fshi.", addr)
                else:
                    send_message("File nuk ekziston.", addr)

            elif msg.startswith("/search"):
                keyword = msg.split(" ", 1)[1] if " " in msg else ""
                files = [f for f in os.listdir(".") if keyword.lower() in f.lower()]
                send_message("Rezultatet:\n" + "\n".join(files), addr)

            elif msg == "exit":
                with lock:
                    if addr in clients:
                      del clients[addr]
                send_message("U shkëpute nga serveri.", addr)
                print(f"{addr} u shkëput.")