import time
import base64
import os
import socket

def get_server_ip():
    default_ip = input(f"🔧 Shkruaj IP-në e serverit [Enter për 127.0.0.1]: ").strip()
    if not default_ip:
        return "127.0.0.1"
    return default_ip

SERVER_IP = get_server_ip()
SERVER_PORT = 5555


def download_file_to_pc(client, server_address, server_filename, save_path):
    try:
        client.sendto(f"/download {server_filename}".encode('utf-8'), server_address)

        data, _ = client.recvfrom(65536)
        response = data.decode('utf-8')

        if response.startswith("FILE_CONTENT:"):
            parts = response.split(":", 2)
            if len(parts) >= 3:
                received_filename = parts[1]
                encoded_content = parts[2]

                file_content = base64.b64decode(encoded_content)

                os.makedirs(os.path.dirname(save_path) if os.path.dirname(save_path) else ".", exist_ok=True)

                with open(save_path, "wb") as f:
                    f.write(file_content)

                print(f"✅ SUCCESS: File '{received_filename}' u shkarkua dhe u ruajt në:")
                print(f"   📁 {os.path.abspath(save_path)}")
                return True
            else:
                print("❌ ERROR: Format i gabuar i përgjigjes nga serveri")
        elif response.startswith("FILE_LARGE:"):
            print("❌ ERROR: File-i është shumë i madh për t'u shkarkuar")
        else:
            print(f"❌ {response}")
        return False

    except Exception as e:
        print(f"❌ Gabim gjatë download-it: {e}")
        return False


def list_server_files(client, server_address):
    client.sendto("/list".encode('utf-8'), server_address)
    data, _ = client.recvfrom(65536)
    response = data.decode('utf-8')
    return response


def read_only_client():
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

    print("Klient READ-ONLY u lidh me serverin")
    print("\n📋 KOMANDAT E LEJUARA:")
    print("  /read <filename>                 - Lexo file nga server")
    print("  /download <filename>             - Shkarko file nga server në PC")
    print("  /list                            - Shfaq file-t në server")
    print("  /search <keyword>                - Kërko file në server")
    print("  /info <filename>                 - Info për file")
    print("  exit                             - Dil")
    print("-" * 60)

    while True:
        try:
            msg = input(">> ").strip()
            if not msg:
                continue

            start_time = time.time()

            allowed_commands = ['/read', '/download', '/list', '/search', '/info', 'exit']
            if not any(msg.startswith(cmd) for cmd in allowed_commands) and msg not in ['exit']:
                print("❌ Komandë e pavlefshme. Komandat e lejuara:")
                print("   /read, /download, /list, /search, /info, exit")
                continue

            if msg.startswith("/download "):
                server_filename = msg.split(" ", 1)[1].strip()
                default_save_path = os.path.join(os.getcwd(), server_filename)
                save_path = input(f"💾 Ruaj në PC si [Enter për '{default_save_path}']: ").strip()
                if not save_path:
                    save_path = default_save_path
                download_file_to_pc(client, server_address, server_filename, save_path)
                continue

            elif msg == "/list":
                files_list = list_server_files(client, server_address)
                print("📁 File-t në server:")
                print(files_list)
                continue

            client.sendto(msg.encode('utf-8'), server_address)

            if msg == "exit":
                break

            data, _ = client.recvfrom(65536)
            response = data.decode('utf-8')

            response_time = (time.time() - start_time) * 1000
            print(f"⏱️ Përgjigja ({response_time:.2f}ms):")
            print(response)
            print("-" * 50)

        except socket.timeout:
            print("⏰ Serveri nuk u përgjigj brenda kohës!")
        except KeyboardInterrupt:
            print("\n👋 Duke u shkëputur...")
            client.sendto("exit".encode(), server_address)
            break
        except Exception as e:
            print(f"❌ Gabim: {e}")
            break

    client.close()


if __name__ == "__main__":
    read_only_client()