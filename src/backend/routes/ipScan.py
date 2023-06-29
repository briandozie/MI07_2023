from flask import Blueprint, request
import nmap

ipScan = Blueprint("ipScan", __name__, url_prefix="/ipScan")

@ipScan.post("/")
def scanIpAddress():
    # retrieve IP address and subnet mask from request body
    data = request.get_json()
    ipAddress = data["ipAddress"]
    subnetMask = data["subnetMask"]
    scanType = data["scanType"]

     # convert subnet mask to CIDR format
    subnetMaskCIDR = sum([bin(int(x)).count('1') for x in subnetMask.split('.')])

    # calculate the range of IP addresses to scan
    startIP = f"{ipAddress}/{subnetMaskCIDR}"
    endIP = f"{ipAddress[:-len(ipAddress.split('.')[-1])]}{int(ipAddress.split('.')[-1])+90}/{subnetMaskCIDR}"

    # scan network for hosts
    nm = nmap.PortScanner()
    nm.scan(hosts=f"{startIP}-{endIP}", arguments=f"-{scanType}")
    hostList = nm.all_hosts()
    return hostList