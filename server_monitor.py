import time
from server_setup import lock,clients

def get_stats():
    with lock:
        lines = []
        lines.append(f"=== SERVER STATS ({time.ctime()}) ===")
        lines.append(f"Numri i klientëve aktivë: {len(clients)}")
        total_bytes = sum(c['bytes'] for c in clients.values())
        lines.append(f"Trafiku total (bytes): {total_bytes}")
        for addr, info in clients.items():
            lines.append(f"{addr} -> msgs: {info['messages']}, "
                         f"bytes: {info['bytes']}, "
                         f"privilege: {info['privilege']}")

        stats = "\n".join(lines)
        print(stats)
        with open("server_stats.txt", "w") as f:
            f.write(stats)
        return stats