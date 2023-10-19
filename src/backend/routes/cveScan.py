from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from app import db
from utilities.databaseFunc import *
from utilities.utilities import *
import subprocess
import os
import signal

cveScan = Blueprint("cveScan", __name__, url_prefix="/cveScan")
pid = 0
cancelled = False

@cveScan.post("/")
def scanTargetCVE():
    global pid, cancelled

    data = request.get_json()
    ipAddress = data["ipAddress"]
    script = data["script"]

    if isHostReachable(ipAddress):


        # Retrieve the command from database
        command = getCommand("CVESCAN")
        command = command.format(
            script = script,
            ipAddress = ipAddress)


        # Run the command using subprocess.Popen
        process = subprocess.Popen(command, shell=True, text=True, stdout=subprocess.PIPE, preexec_fn=os.setsid)

        # Get the process ID (PID)
        pid = process.pid

        # Wait for the process to finish and get the output
        output, _ = process.communicate()

        if not cancelled:
            # Split the output into lines
            cveList = output.splitlines()

            # Takes only the results for easier formatting
            cveList = cveList[4:-2]
            result = '\n'.join(subList.replace('\t', '    ') for subList in cveList)
        
            logActivity("CVE SCAN", ipAddress, script, result)
            cancelled = False

            return jsonify(result) # Convert final output into JSON format  for frontend formatting
        else:
            cancelled = False
            return {}, 204
        
    else:
        return {}, 400

@cveScan.get("/cancel")
def cancelScan():
    global pid, cancelled
    os.killpg(pid, signal.SIGTERM)
    cancelled = True
    return "activity cancelled"

def getCommand(operation):
    collection = db["commands"]
    x = collection.find_one({
        "operation" : operation,
    })

    return x["command"]
