import os
import mss
from datetime import datetime
import time
import socket

# --- Server settings ---
SERVER_HOST = "192.168.1.196"  # Change to your server IP
SERVER_PORT = 5001

# --- Screenshot and send function ---
def send_screenshot(sock, filepath):
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

# --- Main screenshot loop ---
def screenshot_and_send():
    folder = "screenshots"
    os.makedirs(folder, exist_ok=True)

    with mss.mss() as sct, socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((SERVER_HOST, SERVER_PORT))
            print(f"Connected to server at {SERVER_HOST}:{SERVER_PORT}")

            while True:
                # Take screenshot
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                filename = os.path.join(folder, f"screenshot_{timestamp}.png")
                sct.shot(output=filename)
                print(f"Saved {filename}")

                # Send it
                send_screenshot(s, filename)

                time.sleep(1)  # wait 1 second before next screenshot

        except KeyboardInterrupt:
            print("Screenshot loop stopped by user.")
        except Exception as e:
            print("Error:", e)

# --- Run ---
if __name__ == "__main__":
    screenshot_and_send()
