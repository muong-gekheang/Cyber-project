import socket
import os

SERVER_HOST = "192.168.1.196"  # Change to your server IP
SERVER_PORT = 5001
FILES_TO_SEND = ["screenshots/screenshot_2025-11-19_22-11-02.png", "screenshots/screenshot_2025-11-19_22-11-04.png"]  # Add your files here

def send_file(sock, filepath):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    filename = os.path.basename(filepath)
    with open(filepath, 'rb') as f:
        data = f.read()

    # Send 4-byte length of file data
    sock.sendall(len(data).to_bytes(4, 'big'))

    # Send 4-byte length of filename
    sock.sendall(len(filename.encode()).to_bytes(4, 'big'))

    # Send filename
    sock.sendall(filename.encode())

    # Send file data
    sock.sendall(data)
    print(f"Sent {filepath} ({len(data)} bytes)")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((SERVER_HOST, SERVER_PORT))
    print(f"Connected to server at {SERVER_HOST}:{SERVER_PORT}")

    for file_path in FILES_TO_SEND:
        send_file(s, file_path)

    print("All files sent. Closing connection.")