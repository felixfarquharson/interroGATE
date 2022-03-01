import re
import ssl
import socket
import threading
from datetime import datetime, timedelta
import pymongo
from bson import ObjectId

irc_server = "irc.stardust.cx"
irc_port = 6697
irc_nick = "humanduckgame"
irc_key = "**"
channel = '#test'

db = pymongo.MongoClient().db2

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc = ssl.wrap_socket(irc)


def raw_send(data):
    irc.send((data + "\r\n").encode())


def irc_message(msg):
    raw_send("PRIVMSG " + channel + " :" + msg + "\r\n")


irc.connect((irc_server, irc_port))
raw_send("USER " + irc_nick + " 0 * " + ":" + irc_nick + "\r\n")
raw_send("NICK " + irc_nick + "\r\n")
raw_send("JOIN " + channel + "\r\n")

data = ''


def mainloop():
    while 1:
        data = irc.recv(2048).decode("utf8")

        if "ING" in data:
            raw_send("PONG")

        if "PRIVMSG " + channel in data:
            # for msg in data.split("\r\n"):

            if irc_key + "ping" in data:
                irc_message("pong")

            if irc_key + "question" in data:
                a = re.findall(r"\*\*question ([a-zA-Z0-9]{20,30}) (.+)\r\n", data)
                question = a[0][1]
                web_user_id = a[0][0]
                print(f"{web_user_id} {question}")
                if db.user.count_documents({"_id": ObjectId(
                        web_user_id)}) == 1:  # , "last_active": {"$lte": datetime.utcnow() - timedelta(minutes=2)}}) == 1:
                    print("added dia")
                    db.dialog.insert_one({"uid": web_user_id, "question": question, "open": True, "mentioned": False})
                    irc_message(f"()()Asking {web_user_id}: {question}")
                    continue
                irc_message("user has not been online in the last two minutes")


t = threading.Thread(target=mainloop)
t.daemon = True
t.start()

while 1:
    for user in db.user.find({"last_active": {"$gte": datetime.utcnow() - timedelta(minutes=2)}}):
        if not user["mentioned"]:
            irc_message(f"()(){str(user['_id'])} just opened the website()()")
            db.user.update_one({"_id": ObjectId(user["_id"])}, {"$set": {"mentioned": True}})
        for dialog_response in db.dialog_response.find({"uid": user["_id"], "mentioned": False}):
            irc_message(f"(){str(user['_id'])} answered {dialog_response['response']}"
                        f" to question {dialog_response['question']}")
