import socket
import threading
import time

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "0.0.0.0"

SERVER_IP = get_local_ip()
SERVER_PORT = 5555
MAX_CLIENTS = 4
TIMEOUT = 60

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((SERVER_IP, SERVER_PORT))
print(f"🚀 Serveri u startua në {SERVER_IP}:{SERVER_PORT}")
print(f"📡 Klientët mund të lidhen duke përdorur këtë IP")

clients = {}
lock = threading.Lock()

def log_message(addr, msg):
    with open("messages_log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{time.ctime()}] {addr}: {msg}\n")

def check_timeouts():
    while True:
        time.sleep(10)
        now = time.time()
        with lock:
              inactive = [addr for addr, info in
clients.items() if now - info['last_active'] > TIMEOUT]
        for addr in inactive:
                print(f"Klienti {addr} u shkëput për shkak të inaktivitetit.")
                del clients[addr]

timeout_thread = threading.Thread(target=check_timeouts, daemon=True)
timeout_thread.start()
