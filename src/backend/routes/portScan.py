from flask import Blueprint, request
import nmap
portScan = Blueprint("portScan", __name__, url_prefix="/portScan")

@portScan.post("/")
def ScanIpAddress():
    # retrieve IP address and subnet mask from request body
    data = request.get_json()
    ipAddress = data["ipAddress"]
    
    # Scan for open ports 
    nm = nmap.PortScanner() 
    nm.scan(hosts=f"{ipAddress}")
    portList = nm.scaninfo()
    return portList