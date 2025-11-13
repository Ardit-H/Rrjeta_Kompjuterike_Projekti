import os
import time
import base64
from server_setup import server, clients, lock, MAX_CLIENTS, log_message

def send_message(message, addr):
    server.sendto(message.encode('utf-8'), addr)

def handle_messages():
    while True:
        try:
           data, addr = server.recvfrom(65536)
           msg = data.decode('utf-8').strip()

           with lock:
            if addr not in clients:
                if len(clients) >= MAX_CLIENTS:
                    send_message("Serveri është plot. Ju lutem provoni përsëri më vonë.", addr)
                    continue

                privilege = "admin" if msg == "/admin_login" else "read"
                clients[addr] = {
                    "last_active": time.time(),
                    "messages": 0,
                    "bytes": 0,
                    "privilege": privilege,
                    "awaiting_upload": None,
                    "upload_filename": None
                }
                print(f"Klient i ri: {addr} (privilege: {privilege})")

            clients[addr]['last_active'] = time.time()
            clients[addr]['messages'] += 1
            clients[addr]['bytes'] += len(data)

            log_message(addr, msg)

            if msg.upper() == "STATS":
                from server_monitor import get_stats
                stats = get_stats()
                send_message(stats, addr)
                continue

            elif msg.startswith("/list"):
                try:
                    files = os.listdir(".")
                    file_list = "\n".join(files) if files else "Directory është bosh"
                    send_message(file_list, addr)
                except Exception as e:
                     send_message(f"Gabim gjatë listimit: {str(e)}", addr)

            elif msg.startswith("/read"):
                parts = msg.split(" ", 1)
                if len(parts) < 2:
                    send_message("Përdorimi: /read <filename>", addr)
                    continue
                filename = parts[1]
                if not os.path.exists(filename):
                    send_message("File nuk ekziston.", addr)
                    continue
                try:
                    with open(filename, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read(1000)
                    send_message(f"Përmbajtja e {filename}:\n{content}", addr)
                except Exception as e:
                    send_message(f"Gabim gjatë leximit: {str(e)}", addr)

            elif msg.startswith("/write"):
                if clients[addr]['privilege'] != "admin":
                    send_message("Nuk ke privilegje për këtë komandë.", addr)
                    continue

                parts = msg.split(" ", 2)
                if len(parts) < 3:
                    send_message("Përdorimi: /write <filename> <content>", addr)
                    continue

                filename = parts[1]
                content = parts[2]

                try:
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(content)
                    send_message(f"File '{filename}' u shkrua me sukses.", addr)
                except Exception as e:
                    send_message(f"Gabim gjatë shkrimit: {str(e)}", addr)

            elif msg.startswith("/delete"):
                if clients[addr]['privilege'] != "admin":
                    send_message("Nuk ke privilegje për këtë komandë.", addr)
                    continue

                parts = msg.split(" ", 1)
                if len(parts) < 2:
                    send_message("Përdorimi: /delete <filename>", addr)
                    continue

                filename = parts[1]
                if os.path.exists(filename):
                    try:
                        os.remove(filename)
                        send_message(f"File '{filename}' u fshi.", addr)
                    except Exception as e:
                        send_message(f"Gabim gjatë fshirjes: {str(e)}", addr)
                else:
                    send_message("File nuk ekziston.", addr)

            elif msg.startswith("/search"):
                parts = msg.split(" ", 1)
                if len(parts) < 2:
                    send_message("Përdorimi: /search <keyword>", addr)
                    continue

                keyword = parts[1]
                try:
                    files = [f for f in os.listdir(".") if keyword.lower() in f.lower()]
                    result = "Rezultatet:\n" + "\n".join(
                        files) if files else "Nuk u gjet asnjë file me këtë keyword"
                    send_message(result, addr)
                except Exception as e:
                    send_message(f"Gabim gjatë kërkimit: {str(e)}", addr)


            elif msg.startswith("/upload "):
                if clients[addr]['privilege'] != "admin":
                    send_message("Nuk ke privilegje për këtë komandë.", addr)
                    continue
                parts = msg.split(" ", 2)
                if len(parts) < 3:
                    send_message("Përdorimi: /upload <filename> <filedata_base64>", addr)
                    continue
                filename = parts[1]
                encoded_data = parts[2]
                try:
                    file_data = base64.b64decode(encoded_data)
                    with open(filename, "wb") as f:
                        f.write(file_data)
                    send_message(f"SUCCESS: File '{filename}' u ngarkua me sukses në server.", addr)
                except Exception as e:
                    send_message(f"ERROR: Gabim gjatë upload-it: {str(e)}", addr)


            elif msg.startswith("/download "):
                filename = msg.split(" ", 1)[1]
                try:
                    if not os.path.exists(filename):
                        send_message(f"ERROR: File '{filename}' nuk u gjet në server.", addr)
                        continue

                    with open(filename, "rb") as f:
                        file_content = f.read()
                    encoded_content = base64.b64encode(file_content).decode('utf-8')
                    if len(encoded_content) > 50000:
                        send_message("FILE_LARGE:File-i është shumë i madh për download", addr)
                    else:
                        send_message(f"FILE_CONTENT:{filename}:{encoded_content}", addr)


                except Exception as e:
                    send_message(f"ERROR: {str(e)}", addr)

            elif msg.startswith("/info "):
                filename = msg.split(" ", 1)[1]
                if os.path.exists(filename):
                    try:
                        size = os.path.getsize(filename)
                        created = time.ctime(os.path.getctime(filename))
                        modified = time.ctime(os.path.getmtime(filename))
                        send_message(
                            f"ℹ️ Info për '{filename}':\n- Madhësia: {size} bytes\n- Krijuar: {created}\n- Modifikuar: {modified}", addr)

                    except Exception as e:
                        send_message(f"Gabim gjatë marrjes së info: {str(e)}", addr)
                else:
                    send_message(f"File '{filename}' nuk ekziston në server.", addr)

            elif msg == "exit":
                if addr in clients:
                    del clients[addr]
                send_message("U shkëpute nga serveri.", addr)
                print(f"{addr} u shkëput.")

            else:
                if clients[addr]['privilege'] == "admin":
                    send_message(f"Serveri pranoi mesazhin: {msg}", addr)
                else:
                    send_message(
                        "Komandë e pavlefshme. Komandat e lejuara: /read, /list, /search, /info, /download, exit",
                        addr)

        except Exception as e:
            print(f"Gabim në handle_messages: {e}")

if __name__ == "__main__":
    handle_messages()