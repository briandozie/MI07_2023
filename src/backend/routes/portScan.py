from flask import Blueprint, request
import nmap
from app import db
portScan = Blueprint("portScan", __name__, url_prefix="/portScan")

@portScan.post("/")
def PortScan():
    # retrieve IP address and subnet mask from request body
    data = request.get_json()
    ipAddress = data["ipAddress"]
    scanType = data["scanType"]
    
    # retrieve command from database
    command = getCommand("PORTSCAN", scanType)

    # Scan for open ports 
    nm = nmap.PortScanner() 
    nm.scan(hosts=f"{ipAddress}", arguments=command)
    
    ports = formatScanResult(nm)

    # Calculate the total number of items
    totalNumber = len(ports)

    # Create the final JSON structure
    finalJson = {'ports': ports, 'total': totalNumber}

    return finalJson

def getCommand(operation, type):
    collection = db["commands"]
    x = collection.find_one({
        "operation" : operation,
        "type": type,
        })

    return x["command"]

def formatScanResult(scanner):
    # extract the indexes for the columns
    rows = scanner.csv().strip().split("\n")
    categories = rows[0].split(";")
    max_lengths = [len(category) for category in categories]
    rows_data = [row.split(";") for row in rows[1:]]

    # Only keep specified columns
    keep_columns = ["host", "protocol", "port", "state"]
    keep_indices = [categories.index(col) for col in keep_columns]
    categories = [categories[i] for i in keep_indices]
    max_lengths = [max_lengths[i] for i in keep_indices]
    rows_data = [[row[i] for i in keep_indices] for row in rows_data]

    # Convert the list of lists to a list of dictionaries
    ports = [{'host': item[0], 'protocol': item[1], 'port': item[2], 'status': item[3]} for item in rows_data]

    return ports