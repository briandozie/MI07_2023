from flask import Blueprint, request, jsonify
from utilities.databaseFunc import *
import signal
import subprocess
import time
import os
import threading
import datetime

dosAttack = Blueprint("dosAttack", __name__, url_prefix="/dosAttack")
latencyPingList = []

@dosAttack.post("/")
def DOSAttack():
    data = request.get_json()
    ipAddress = data["ipAddress"]
    portNumber = data["portNumber"]
    packetSize = data["packetSize"]
    attackType = data["attackType"]
    duration = int(data["duration"])
    
    # get dos command from database
    command = getCommand("DOS", "PINGFLOOD")
    command = command.format(
        attackType=attackType,
        packetSize=packetSize,
        portNumber=portNumber,
        ipAddress=ipAddress)
    
    # create thread for latency polling
    latencyCheck = threading.Thread(target=checkLatencyPeriodically, args=(ipAddress, duration))
    latencyCheck.start()
    
    # create thread for dos attack
    attack = threading.Thread(target=dos, args=(command, duration))
    attack.start()

    # wait for threads to finish
    attack.join()
    latencyCheck.join()

    # log dos attack details to database
    logActivityDOS("DOS ATTACK", data, latencyPingList)
    latencyPingList.clear()

    return ""

@dosAttack.post("/latency")
def checkLatency():
    if len(latencyPingList) > 0:
        return latencyPingList[-1]
    else:
        return ""

def checkLatencyPeriodically(ipAddress, duration):
    command = getCommand("PING", "LATENCY")
    command = command.format(ipAddress=ipAddress)
    startTime = datetime.datetime.now()
    duration = datetime.timedelta(seconds=duration)

    # poll for latency every 5 seconds
    while datetime.datetime.now() - startTime < duration:
        latency(command)
        time.sleep(5)
    
def latency(command):
    pingCommand = subprocess.Popen(command, stdout=subprocess.PIPE, text=True, shell=True)
    output, _ = pingCommand.communicate()  # Capture the output and wait for the process to finish

    lines = output.splitlines()
    line = lines[1]

    # append latency ping result to list
    if "time" in line:
        latencyPingList.append('[PING SUCCESS] ' + line)
    else:
        latencyPingList.append('[PING FAILED] ' + line)

def dos(command, duration):
    # carry out attack for specified duration
    dosCommand = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, text=True, preexec_fn=os.setsid)
    time.sleep(duration) 
    os.killpg(os.getpgid(dosCommand.pid), signal.SIGTERM)
