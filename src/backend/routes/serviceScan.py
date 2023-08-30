from flask import Blueprint, request
import nmap
serviceScan = Blueprint("serviceScan", __name__, url_prefix="/serviceScan")

@serviceScan.post("/")
def ServiceScan():
    # retrieve IP address and subnet mask from request body
    data = request.get_json()
    ipAddress = data["ipAddress"]
    scanType = data["scanType"]
    
    # Scan for open ports 
    nm = nmap.PortScanner() 
    nm.scan(hosts=f"{ipAddress}", arguments=f"-{scanType} -D RND:30")
    
    # extract the indexes for the columns
    rows = nm.csv().strip().split("\n")
    categories = rows[0].split(";")
    max_lengths = [len(category) for category in categories]
    rows_data = [row.split(";") for row in rows[1:]]

    # Only keep specified columns
    keep_columns = ["host", "port", "name", "product", "extrainfo", "version"]
    keep_indices = [categories.index(col) for col in keep_columns]
    categories = [categories[i] for i in keep_indices]
    max_lengths = [max_lengths[i] for i in keep_indices]
    rows_data = [[row[i] for i in keep_indices] for row in rows_data]

    # Convert the list of lists to a list of dictionaries
    ports = [{'host': item[0], 'protocol': item[1], 'port': item[2], 'product': item[3], 'extrainfo': item[4], 'version': item[5]} for item in rows_data]

    # Calculate the total number of items
    totalNumber = len(ports)

    # Create the final JSON structure
    finalJson = {'ports': ports, 'total': totalNumber}

    return finalJson