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
    columns = ["host", "protocol", "port", "state"]
    indexes = [i for i, category in enumerate(rows[0].split(";")) if category in columns]
    
    # extract the element for each column
    data = []
    for row in rows:
      row_data = row.split(";")
      selected_data = [row_data[i].strip() for i in indexes]
      data.append(selected_data)
    
    # this is to beautify the output to be more readable
    max_lengths = [len(column) for column in columns]
    for row_data in data:
      for i, element in enumerate(row_data):
        max_lengths[i] = max(max_lengths[i], len(element))
    
    for i, column in enumerate(columns):
      print(column.ljust(max_lengths[i]), end=" ")
    print()

    for row_data in data:
      for i, element in enumerate(row_data):
        print(element.ljust(max_lengths[i]), end=" ")
      print()
    
    return None