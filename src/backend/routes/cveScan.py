from flask import Blueprint, request, jsonify
import nmap
import subprocess

cveScan = Blueprint("cveScan", __name__, url_prefix="/cveScan")

@cveScan.post("/")
def scanTargetCVE():
    data = request.get_json()
    ipAddress = data["ipAddress"]
    scanType = data["scanType"]
    script = data["script"]

    # Scan for CVE in target and store it in a list
    cveList = subprocess.run([f"nmap -{scanType} --script {script} {ipAddress}"], 
                          shell=True, text=True, stdout=subprocess.PIPE).stdout.splitlines()
    
    # Takes only the results for easier formatting
    results = []
    for line in cveList[4:-2]:
        columns = line.split('\t')
        host = columns[0]
        port = columns[1]
        cve = columns[2]
        cveLink = columns[3]
        results.append({"host": host, "port": port, "cve": cve, "cveLink": cveLink})

    # Convert final output into JSON format for frontend formatting
    return jsonify(results)