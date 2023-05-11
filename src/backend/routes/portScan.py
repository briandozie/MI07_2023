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
    # Format the output
    #my_lines = nm.csv.splitline()
    #my_list = []
   # for line in range(my_lines):
        #line_list = line.split(";")
      #  my_list.extend(line_list)
    
    return nm.csv