
# STAM listener (Python)

# File: stam_listener.py

import socket
import threading
import json

HOST = '127.0.0.1'  # localhost
PORT = 9090         # default listener port for STAM

flow_cache = {}

def handle_client(conn, addr):
    print(f"[+] Connected by {addr}")
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            try:
                message = json.loads(data.decode())
                flow_id = message.get("flow_hash")
                timestamp = message.get("timestamp")
                print(f"[*] Received digest for Flow ID: {flow_id} at {timestamp}")
                flow_cache[flow_id] = timestamp
            except Exception as e:
                print(f"[!] Failed to process digest: {e}")

def start_listener():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen()
        print(f"[*] STAM Listener active on {HOST}:{PORT}")
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

if __name__ == '__main__':
    print("[+] Starting STAM Listener...")
    start_listener()
