import time
import threading
from server_setup import lock, clients


def get_stats():
    with lock:
        lines = []
        lines.append(f"=== SERVER STATS ({time.ctime()}) ===")
        lines.append(f"Numri i klientëve aktivë: {len(clients)}")
        total_bytes = sum(c['bytes'] for c in clients.values())
        total_messages = sum(c['messages'] for c in clients.values())
        lines.append(f"Mesazhet totale: {total_messages}")
        lines.append(f"Trafiku total (bytes): {total_bytes}")
        lines.append("\nKlientët aktivë:")

        for addr, info in clients.items():
            lines.append(f"{addr} -> msgs: {info['messages']}, "
                         f"bytes: {info['bytes']}, "
                         f"privilege: {info['privilege']}, "
                         f"last_active: {time.ctime(info['last_active'])}")

        stats = "\n".join(lines)
        print(stats)

        with open("server_stats.txt", "w", encoding="utf-8") as f:
            f.write(stats)
        return stats

def periodic_monitor(interval=30):
        while True:
            time.sleep(interval)
            get_stats()

monitor_thread = threading.Thread(target=periodic_monitor, daemon=True)
monitor_thread.start()