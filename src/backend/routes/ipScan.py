from flask import Blueprint, request
import nmap

ipScan = Blueprint("ipScan", __name__, url_prefix="/ipScan")

@ipScan.post("/")
def scanIpAddress():
    # retrieve IP address and subnet mask from request body
    data = request.get_json()
    ips = data.get("ips", [])
    ipRange = data["ipRange"]
    subnetMask = data["subnetMask"]
    scanType = data["scanType"]
    
    startIP, endIP = ipRange.split("-")
    nm = nmap.PortScanner()
    hostList = []
     # Scan individual IP addresses
    for ip in ips:
        nm.scan(hosts=ip, arguments=f"-{scanType}")
        hostList.extend(nm.all_hosts())

    # scan network for hosts
    if ipRange:
        nm.scan(hosts=f"{startIP}-{endIP}", arguments=f"-{scanType}")
        hostList = nm.all_hosts()
    return hostList