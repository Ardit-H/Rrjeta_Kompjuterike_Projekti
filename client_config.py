import socket


def get_server_ip():
    """Kërkon IP-në e serverit nga përdoruesi"""
    print("=" * 50)
    print("KONFIGURIMI I KLIENTIT")
    print("=" * 50)

    # Sugjerim automatik për IP-në lokale
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        print(f"IP-ja juaj lokale: {local_ip}")
    except:
        local_ip = "127.0.0.1"

    default_server_ip = input(
        f"Shkruaj IP-në e serverit [sugjerim: {local_ip.replace(local_ip.split('.')[-1], '1')}]: ").strip()

    if not default_server_ip:
        # Sugjeron IP-në e router-it (xxx.xxx.xxx.1)
        default_server_ip = local_ip.replace(local_ip.split('.')[-1], '1')

    SERVER_PORT = 5555

    return default_server_ip, SERVER_PORT


def test_connection(server_ip, server_port):
    """Teston lidhjen me serverin"""
    try:
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        test_socket.settimeout(3)
        test_socket.sendto("test".encode(), (server_ip, server_port))
        data, _ = test_socket.recvfrom(1024)
        test_socket.close()
        return True
    except:
        return False