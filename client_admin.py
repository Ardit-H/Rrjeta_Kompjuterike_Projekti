import socket
import time
import base64
import os

def get_server_ip():
    """Pyet për IP-në e serverit"""
    default_ip = input(f"🔧 Shkruaj IP-në e serverit [Enter për 127.0.0.1]: ").strip()
    if not default_ip:
        return "127.0.0.1"
    return default_ip

SERVER_IP = get_server_ip()
SERVER_PORT = 5555

def upload_file_from_pc(client, server_address, file_path):
    """Mer file nga PC dhe e dërgon në server"""
    try:
        if not os.path.exists(file_path):
            print(f"ERROR: File '{file_path}' nuk ekziston!")
            return False

        filename = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)

        print(f"Po ngarkoj: {filename} ({file_size} bytes) nga {file_path}")

        with open(file_path, "rb") as f:
            file_data = f.read()

        encoded_data = base64.b64encode(file_data).decode('utf-8')

        message = f"/upload {filename} {encoded_data}"
        client.sendto(message.encode('utf-8'), server_address)

        data, _ = client.recvfrom(65536)
        response = data.decode('utf-8')
        print(response)
        return True

    except Exception as e:
        print(f"Gabim gjatë upload-it: {e}")
        return False

def download_file_to_pc(client, server_address, server_filename, save_path):
    """Shkarkon file nga server dhe e ruan në PC"""
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

def write_to_file(client, server_address, filename, content):
    """Shkruan content në file në server"""
    try:
        message = f"/write {filename} {content}"
        client.sendto(message.encode('utf-8'), server_address)

        data, _ = client.recvfrom(65536)
        response = data.decode('utf-8')
        print(response)
        return True
    except Exception as e:
        print(f"❌ Gabim gjatë shkrimit: {e}")
        return False

def list_server_files(client, server_address):
    """Liston file-t në server"""
    client.sendto("/list".encode('utf-8'), server_address)
    data, _ = client.recvfrom(65536)
    response = data.decode('utf-8')
    return response

def admin_client():
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

    print("🚀 Klient ADMIN u lidh me serverin")
    print("\n📋 KOMANDAT:")
    print("  /upload <path_i_plotë_në_PC>     - Ngarko file nga PC në server")
    print("  /download <filename>             - Shkarko file nga server në PC")
    print("  /write <filename> <content>      - Shkruaj në file në server")
    print("  /list                            - Shfaq file-t në server")
    print("  /delete <filename>               - Fshi file nga server")
    print("  /search <keyword>                - Kërko file në server")
    print("  /info <filename>                 - Info për file")
    print("  /read <filename>                 - Lexo file nga server")
    print("  STATS                            - Statistikat e serverit")
    print("  exit                             - Dil")
    print("  <çdo mesazh tjetër>              - Dërgo mesazh të thjeshtë")
    print(f"\n📁 Folderi aktual në PC: {os.getcwd()}")
    print("-" * 60)

    while True:
        try:
            msg = input(">> ").strip()
            if not msg:
                continue

            start_time = time.time()

            if msg.startswith("/upload "):
                file_path = msg.split(" ", 1)[1].strip()
                file_path = file_path.replace('\\', '/')
                upload_file_from_pc(client, server_address, file_path)
                continue

            elif msg.startswith("/download "):
                 server_filename = msg.split(" ", 1)[1].strip()
                 default_save_path = os.path.join(os.getcwd(), server_filename)
                 save_path = input(f"💾 Ruaj në PC si [Enter për '{default_save_path}']: ").strip()
                 if not save_path:
                     save_path = default_save_path
                 download_file_to_pc(client, server_address, server_filename, save_path)
                 continue

            elif msg.startswith("/write "):
                parts = msg.split(" ", 2)
                if len(parts) >= 3:
                    filename = parts[1]
                    content = parts[2]
                    write_to_file(client, server_address, filename, content)
                else:
                    print("❌ Përdorimi: /write <filename> <content>")
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
    admin_client()