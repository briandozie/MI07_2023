from flask import Blueprint, request, jsonify
from utilities.databaseFunc import *
import signal
import subprocess
import time
import os
from pymongo import MongoClient
from app import db
import threading
from multiprocessing import Process

dosAttack = Blueprint("dosAttack", __name__, url_prefix="/dosAttack")
latencyPingList = []

@dosAttack.post("/")
def SYNFloodAttack():
    data = request.get_json()
    ipAddress = data["ipAddress"]
    portNumber = data["portNumber"]
    packetSize = data["packetSize"]
    attackType = data["attackType"]
    duration = int(data["duration"])
    latencyPingList.clear()

    command = getCommand("DOS", "PINGFLOOD")
    command = command.format(
        attackType=attackType,
        packetSize=packetSize,
        portNumber=portNumber,
        ipAddress=ipAddress)
    
    # launch dos attack on seperate thread
    attack = threading.Thread(target=dos, args=(command, duration))
    attack.start()
    attack.join()

    
    logActivityDOS("DOS ATTACK", data, latencyPingList)

    return ""

@dosAttack.post("/latency")
def checkLatency():
    data = request.get_json()
    ipAddress = data["ipAddress"]

    command = getCommand("PING", "LATENCY")
    command = command.format(ipAddress=ipAddress)

    result = []

    ping = threading.Thread(target=latency, args=(command, result))
    ping.start()
    ping.join()

    return latencyPingList[-1]

    
def latency(command, result):
    pingCommand = subprocess.Popen(command, stdout=subprocess.PIPE, text=True, shell=True)
    output, _ = pingCommand.communicate()  # Capture the output and wait for the process to finish

    lines = output.splitlines()
    line = lines[1]

    if "time" in line:
        latencyPingList.append('[PING SUCCESS] ' + line)
    else:
        latencyPingList.append('[PING FAILED] ' + line)

def dos(command, duration):
    dosCommand = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, text=True, preexec_fn=os.setsid)
    
    # carry out attack for specified duration
    time.sleep(duration) 
    os.killpg(os.getpgid(dosCommand.pid), signal.SIGTERM)

