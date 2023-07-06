from flask import Blueprint, request
import subprocess

ipMasking = Blueprint("ipMasking", __name__, url_prefix="/ipMasking")

@ipMasking.post("/")
def scanTargetCVE():
    data = request.get_json()
    ipAddress = data["ipAddress"]
    scanType = data["scanType"]
    NumOfIps = data["NumOfIps"]

    # Standard scan on target and store it in a list
    TestList = subprocess.run(["powershell", f"nmap -{scanType} -D RND:{NumOfIps} {ipAddress}"], 
                          shell=True, text=True, stdout=subprocess.PIPE).stdout.splitlines()
    
    # Function to remove \t in list elements (Needs refinement)
    #result = ' '.join(subList.replace('\t', '    ') for subList in cveList)

    return TestList