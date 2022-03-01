import json
from datetime import datetime

from bottle import request, route, run, template
import pymongo

from bson import ObjectId

db = pymongo.MongoClient().db2


@route("/")
def home():
    return template("home")


@route("/api/init")
def init():
    x = db["user"].insert_one({"last_active": datetime.utcnow(), "mentioned": False})
    return {"id": str(x.inserted_id)}


@route("/api/poll", method="post")
def poll():
    dat = request.body.read().decode("utf8")
    print(request.body.read().decode("utf8"))
    request_data = json.loads(dat)

    db.user.update_one({"_id": ObjectId(request_data["id"])}, {"$set":{"last_active": datetime.utcnow()}})

    if not db.user.count_documents({"_id": ObjectId(request_data.get("id", ""))}) == 1:
        return {"error": "cannot find user, refresh"}

    dia = db.dialog.find({"uid": request_data["id"], "open": True})#, "mentioned": False})
    db.dialog.update_many({"uid": request_data["id"], "open": True, "mentioned": False}, {"$set": {"mentioned": True}})
    return {"dialog": [{"id": str(x["_id"]), "question": x["question"]} for x in dia]}

#
# @route("/api/submit")
# def submit():
#     request_data = json.loads(request.body)
#
#     if not db.user.count_documents({"_id": ObjectId(request_data.get("id", ""))}) == 1:
#         return {"error": "cannot find user, refresh"}
#
#     if request_data.get("method", None):
#         if request_data["method"] == "dialog":
#             db.dialog.update_one({"open": True, "uid": request_data["id"]},
#                                  {"$set": {"open": False, "value": request_data["value"]}})
#             return {"success": True}
#
#         #elif request_data["method"] == "freetext":
#         #elif request_data["method"] == "choice":
#         #elif request_data["method"] == "close":
#         #else:
#         #    return
#     return {"success": False}


run(host="80.85.85.52", port=80, debug=True)
