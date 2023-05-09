from flask import Blueprint, request
import nmap
portScan = Blueprint("portScan", __name__, url_prefix="/portScan")

@portScan.post("/")
def ScanIpAddress():
    # retrieve IP address and subnet mask from request body
    data = request.get_json()
    ipAddress = data["ipAddress"]
    subnetMask = data["subnetMask"]
    scanType = data["scanType"]
    
    # Scan for open ports 
    nm = nmap.PortScanner() 
    nm.scan(hosts=f"{ipAddress}/{subnetMask}", arguments=f"-{scanType}")
    portList = nm.scaninfo()
    return portList