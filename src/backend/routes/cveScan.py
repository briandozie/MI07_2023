from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from app import db
from utilities.databaseFunc import *
import subprocess

cveScan = Blueprint("cveScan", __name__, url_prefix="/cveScan")

@cveScan.post("/")
def scanTargetCVE():
    data = request.get_json()
    ipAddress = data["ipAddress"]
    script = data["script"]

    # Retrieve the command from database
    command = getCommand("CVESCAN")
    command = command.format(
        script = script,
        ipAddress = ipAddress)

    # Scan for CVE in target and store it in a list
    cveList = subprocess.run(command, shell=True, text=True, 
                             stdout=subprocess.PIPE).stdout.splitlines()
    
    # Takes only the results for easier formatting
    cveList = cveList[4:-2]
    result = '\n'.join(subList.replace('\t', '    ') for subList in cveList)
   
    logActivity("CVE SCAN", ipAddress, script, result)
    
    return jsonify(result) # Convert final output into JSON format for frontend formatting

def getCommand(operation):
    collection = db["commands"]
    x = collection.find_one({
        "operation" : operation,
    })

    return x["command"]
