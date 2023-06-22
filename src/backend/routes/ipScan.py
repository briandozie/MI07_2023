from flask import Blueprint, request
import nmap

ipScan = Blueprint("ipScan", __name__, url_prefix="/ipScan")

@ipScan.post("/")
def scanIpAddress():
    # retrieve IP address and subnet mask from request body
    data = request.get_json()
    ipAddress = data["ipAddress"]
    subnetMask = data["subnetMask"]
    scanType = data["scanType"]

    # scan network for hosts
    nm = nmap.PortScanner()
    hostList = []

    # Scan IP address range
    if "-" in ipAddress:
        start_ip, end_ip = ipAddress.split("-")
        nm.scan(hosts=f"{start_ip}-{end_ip}/{subnetMask}", arguments=f"-{scanType}")
        hostList.extend(nm.all_hosts())
    else:
        # Scan multiple IP addresses
        for ip in ipAddress:
            nm.scan(hosts=f"{ip}/{subnetMask}", arguments=f"-{scanType}")
            hostList.extend(nm.all_hosts())
    return hostList