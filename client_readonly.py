import socket
import time
from client_config import get_server_ip, test_connection


def readonly_client():
    SERVER_IP, SERVER_PORT = get_server_ip()
    server_address = (SERVER_IP, SERVER_PORT)

    print(f"Duke u lidhur me serverin {SERVER_IP}:{SERVER_PORT}...")

    # Testo lidhjen
    if not test_connection(SERVER_IP, SERVER_PORT):
        print(f"❌ Nuk mund të lidhem me serverin {SERVER_IP}:{SERVER_PORT}!")
        print("Kontrollo:")
        print("1. A është serveri i startuar?")
        print("2. A është IP-ja e saktë?")
        print("3. A janë të ndryshme firewall settings?")
        return

    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print("✅ Klient READ-ONLY u lidh me serverin.")
    print("Komandat: /list, /read <file>, /search <keyword>, /info <file>, STATS, exit")
    print("-" * 50)

    while True:
        try:
            msg = input(">> ").strip()
            if not msg:
                continue

            start_time = time.time()
            client.sendto(msg.encode('utf-8'), server_address)

            if msg == "exit":
                break
            data, _ = client.recvfrom(65536)
            response = data.decode('utf-8')

            response_time = (time.time() - start_time) * 1000
            print(f"Përgjigja ({response_time:.2f}ms):")
            print(response)
            print("-" * 50)
        except socket.timeout:
            print("Serveri nuk u përgjigj brenda kohës!")
        except KeyboardInterrupt:
            print("\nDuke u shkëputur...")
            client.sendto("exit".encode(), server_address)
            break
        except Exception as e:
            print(f"Gabim: {e}")
            break

    client.close()
    print("Lidhja u mbyll.")

if __name__ == "__main__":
    readonly_client()