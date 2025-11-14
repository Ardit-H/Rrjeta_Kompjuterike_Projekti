# UDP File Management System – Server & Client

A Computer Networks project implementing a UDP-based client–server system with file management, admin permissions, monitoring, file transfer, timeout handling, and real-time traffic statistics.

---

##  Project Overview

This project implements a UDP-based client–server system where multiple clients can connect to a single server and perform different operations depending on their permissions.  
Admin clients have full access (read, write, upload, delete), while regular clients have read-only access.

The server additionally monitors traffic, logs messages, tracks active connections, and handles inactive clients through timeouts.

---

##  Project Structure

/server
│── server_main.py
│── server_setup.py
│── server_core.py
│── server_monitor.py

/client
│── client_admin.py
│── client_readonly.py


---

##  Features

###  Server Features
- Defines its own **IP address** and **port**
- Accepts multiple client connections
- Rejects or queues new connections when maximum threshold is reached
- Processes requests from each connected client
- Logs all messages for monitoring
- Disconnects inactive clients (timeout)
- Automatically restores connection if client reconnects
- Provides **full file access** to admin clients
- Implements traffic monitoring:
  - Active connections count
  - Active clients’ IPs
  - Number of messages per client
  - Total bytes sent/received


---

##  Client Types

###  Admin Client (full access)

Admin users can execute:

| Command | Description |
|---------|-------------|
| `/list` | List files in a directory |
| `/read <filename>` | Read file contents |
| `/upload <filename>` | Upload file to server |
| `/download <filename>` | Download a file |
| `/delete <filename>` | Delete a file |
| `/search <keyword>` | Search filenames for a keyword |
| `/info <filename>` | Show file size and timestamps |

Admin users also receive **faster response time**.

---

###  Read-only Client

Regular users can:
- Read server responses
- Execute only safe read-based commands
- No upload/delete/modify permissions

---

##  Networking Requirements

- All communication uses **UDP sockets**:
  - `AF_INET`
  - `SOCK_DGRAM`
- Client must connect using correct server IP + port
- Server handles multiple clients simultaneously

---

## File Operations

Supported operations:

- File upload (client → server)
- File download (server → client)
- Directory listing
- Search filenames
- File information metadata
- Reading file content

File transfers use:
- UDP chunking
- Acknowledgments
- Resending on missed packets

---

## Timeout Handling

If a client does not send messages for a defined interval:

- Server removes the client from active list  
- When the client reconnects, server restores connection automatically  

---

##  Example Server Statistics Output

Active Connections: 3
Active Client IPs:

192.168.1.10

192.168.1.15

192.168.1.22

Messages Per Client:

192.168.1.10 → 14 messages

192.168.1.15 → 8 messages

192.168.1.22 → 26 messages

Total Traffic:

Sent: 85 KB

Received: 112 KB


---

##  How to Run the System

###  Start the Server

python server_main.py

###  Start Admin Client

python client_admin.py

###  Start Read-only Client

python client_readonly.py


---

##  Requirements
- Python 3.x
- Windows / Linux / macOS
- Stable local network
- Basic understanding of UDP

---





