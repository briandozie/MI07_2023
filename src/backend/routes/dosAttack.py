from flask import Blueprint, request
import nmap

dosAttack = Blueprint("dosAttack", __name__, url_prefix="/dosAttack")

# @dosAttack.post("/")
#   # def slowlorisDosAttack():