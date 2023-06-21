from flask import Blueprint, request
import nmap

cveScan = Blueprint("cveScan", __name__, url_prefix="/cveScan")

@cveScan.post("/")
def scanIpAddress():
    data = request.get_json()
    ipAddress = data["ipAddress"]
    scanType = data["scanType"]
    script = data["script"]

    # Scan for CVE in target
    nm = nmap.PortScanner()
    nm.scan(hosts=f"{ipAddress}", arguments=f"-{scanType} --script {script}")
    
    return nm.csv()