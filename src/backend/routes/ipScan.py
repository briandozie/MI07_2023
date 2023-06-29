from flask import Blueprint, request
import nmap

ipScan = Blueprint("ipScan", __name__, url_prefix="/ipScan")

@ipScan.post("/")
def scanIpAddress():
    # retrieve start address, end address, subnet mask, and scan type from request body
    data = request.get_json()
    startAddress = data["startAddress"]
    endAddress = data["endAddress"]
    subnetMask = data["subnetMask"]
    scanType = data["scanType"]

    # scan network for hosts
    nm = nmap.PortScanner()

    # Convert the start and end addresses to integers for iteration
    start = int(startAddress.split('.')[-1])
    end = int(endAddress.split('.')[-1])

    hostList = []

    # Iterate over the range of hosts and scan each IP address
    for i in range(start, end + 1):
        currentAddress = startAddress.rsplit('.', 1)[0] + '.' + str(i)
        nm.scan(hosts=f"{currentAddress}/{subnetMask}", arguments=f"-{scanType}")
        hostList.append(nm.all_hosts())

    return hostList