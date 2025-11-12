from server_core import handle_messages
import threading

if __name__ == "__main__":
    print("Duke startuar serverin...")
    print("Serveri është gati për lidhje!")
    print("Shkruaj 'STATS' në terminal për të parë statistikat aktuale")

    core_thread = threading.Thread(target=handle_messages, daemon=True)
    core_thread.start()

    while True:
        cmd = input("Server command: ")
        if cmd.upper() == "STATS":
            from server_monitor import get_stats

            get_stats()
        elif cmd.upper() == "EXIT":
            print("Mbyllja e serverit...")
            break
        else:
            print("Komandat e disponueshme: STATS, EXIT")