from flask import Blueprint, request
import nmap

cveScan = Blueprint("cveScan", __name__, url_prefix="/cveScan")

@cveScan.post("/")
def scanIpAddress():
    data = request.get_json()
    ipAddress = data["ipAddress"]
    subnetMask = data["subnetMask"]
    scanType = data["scanType"]

    # Scan for CVE in target
    nm = nmap.PortScanner()
    nm.scan(hosts=f"{ipAddress}", arguments=f"-{scanType}")