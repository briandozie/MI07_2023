from flask import Blueprint, request, jsonify
from app import db

dashboard = Blueprint("dashboard", __name__, url_prefix="/dashboard")

@dashboard.get("/history")
def getHistory():
  collection = db["activity"]
  queryResult = collection.find({}, {
     "activity" : 1,
     "date": 1,
     "time": 1,
     "target": 1}).sort([("_id", -1)]).limit(5)

  # Create an empty list to store the documents
  historyData = []

  for entry in queryResult:  # Iterate through the cursor
      entry["_id"] = str(entry["_id"])
      historyData.append(entry)

  return jsonify(historyData)