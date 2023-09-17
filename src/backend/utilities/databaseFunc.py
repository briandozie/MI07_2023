from datetime import datetime
from app import db

def getCommand(operation, type):
    collection = db["commands"]
    x = collection.find_one({
        "operation" : operation,
        "type": type,
        })
    return x["command"]

# method to log the activity to database
def logActivity(activity, targetIP, scanType, json):
    collection = db["activity"]
    collection.insert_one({
        'date': datetime.now().strftime("%d/%m/%Y"),
        'time': datetime.now().strftime("%H:%M:%S"),
        'activity': activity,
        'type': scanType,
        'target': targetIP,
        'result': json,
    })

def logActivityDOS(activity, data, latency):
    ipAddress = data["ipAddress"]
    portNumber = data["portNumber"]
    packetSize = data["packetSize"]
    attackType = data["attackTypeLabel"]
    duration = int(data["duration"])

    collection = db["activity"]
    collection.insert_one({
      'date': datetime.now().strftime("%d/%m/%Y"),
      'time': datetime.now().strftime("%H:%M:%S"),
      'activity': activity,
      'type': attackType,
      'target ': ipAddress,
      'port': portNumber,
      'duration': duration,
      'packetSize': packetSize,
      'result': latency,
  })