from flask import Blueprint, request
import nmap
portScan = Blueprint("portScan", __name__, url_prefix="/portScan")

@portScan.post("/")
def ScanIpAddress():
    # retrieve IP address and subnet mask from request body
    data = request.get_json()
    ipAddress = data["ipAddress"]
    scanType = data["scanType"]
    
    # Scan for open ports 
    nm = nmap.PortScanner() 
    nm.scan(hosts=f"{ipAddress}", arguments=f"-{scanType}")
    
    # extract the indexes for the columns
    rows = nm.csv().strip().split("\n")
    categories = rows[0].split(";")
    max_lengths = [len(category) for category in categories]
    rows_data = [row.split(";") for row in rows[1:]]

    # Only keep specified columns
    keep_columns = ["host", "protocol", "port", "state"]
    keep_indices = [categories.index(col) for col in keep_columns]
    categories = [categories[i] for i in keep_indices]
    max_lengths = [max_lengths[i] for i in keep_indices]
    rows_data = [[row[i] for i in keep_indices] for row in rows_data]

    # Pad empty elements to match category length
    for row_data in rows_data:
        for i, element in enumerate(row_data):
            if element == "":
                row_data[i] = " " * (max_lengths[i] - len(categories[i]))
            else:
                max_lengths[i] = max(max_lengths[i], len(element))

    # Build output string
    output = ""
    output += "".join(category.ljust(max_lengths[i] + 2) for i, category in enumerate(categories)) + "\n"
    for row_data in rows_data:
        output += "".join(element.ljust(max_lengths[i] + 2) for i, element in enumerate(row_data)) + "\n"

    return output