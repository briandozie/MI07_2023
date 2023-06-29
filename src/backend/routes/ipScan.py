from flask import Blueprint, request
import nmap

ipScan = Blueprint("ipScan", __name__, url_prefix="/ipScan")

@ipScan.post("/")
def scanIpAddress():
    # retrieve IP address and subnet mask from request body
    data = request.get_json()
    startIP = data["startIP"]
    endIP = data["endIP"]
    subnetMask = data["subnetMask"]
    scanType = data["scanType"]

    # scan network for hosts
    nm = nmap.PortScanner()
    nm.scan(hosts=f"{startIP}-{endIP}", arguments=f"-{scanType}")
    hostList = nm.all_hosts()
    return hostList