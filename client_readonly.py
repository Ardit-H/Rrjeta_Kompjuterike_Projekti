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

if __name__ == "__main__":
    readonly_client()