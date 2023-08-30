from flask import Blueprint, request, jsonify
import subprocess

cveScan = Blueprint("cveScan", __name__, url_prefix="/cveScan")

@cveScan.post("/")
def scanTargetCVE():
    data = request.get_json()
    ipAddress = data["ipAddress"]
    scanType = data["scanType"]
    script = data["script"]

    # Scan for CVE in target and store it in a list
    cveList = subprocess.run([f"nmap -{scanType} -D RND,RND,ME --script {script} {ipAddress}"], 
                          shell=True, text=True, stdout=subprocess.PIPE).stdout.splitlines()
    
    # Takes only the results for easier formatting
    cveList = cveList[4:-2]
    result = '\n'.join(subList.replace('\t', '    ') for subList in cveList)
   
    # Convert final output into JSON format for frontend formatting
    return jsonify(result)