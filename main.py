import json
from datetime import datetime

from bottle import request, route, run, template, install
from bottle_mongo import MongoPlugin

install(MongoPlugin(uri="mongodb://127.0.0.1", db="db"))

@route("/")
def home():
    return template("home")

@route("api/init")
def init(db):
    x = db["user"].insert_one({"last_active": datetime.utcnow()})
    return {"id": x.inserted_id}

@route("/api/poll", method="POST")
def poll(db):
    request_data = json.loads(request.body)

    if not db.user.find_one({"_id": request_data.get("id", "")}).exists():
        return {"error": "cannot find user, refresh"}

    dia = db.dialog.find({"uid": request_data["id"], "open": True})
    return {"dialog": [dia]}

@route("/api/submit")
def submit(db):
    request_data = json.loads(request.body)

    if not db.user.find_one({"_id": request_data.get("id", "")}).exists():
        return {"error": "cannot find user, refresh"}

    if request_data.get("method", None):
        db.user.update_one({"_id": request_data["id"]}, {"last_active": datetime.utcnow()})

        if request_data["method"] == "dialog":
            db.dialog.update_one({"open": True, "uid": request_data["id"]},
                                 {"open": False, "value": request_data["value"]})
            return {"success": True}

        #elif request_data["method"] == "freetext":
        #elif request_data["method"] == "choice":
        #elif request_data["method"] == "close":
        #else:
        #    return
    return {"success": False}