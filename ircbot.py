import ssl
import socket
import threading
from datetime import datetime, timedelta
import pymongo

irc_server = "irc.stardust.cx"
irc_port = 6697
irc_nick = "humanduckgame"
irc_key = "**"
channel = '#test'

db = pymongo.MongoClient().db

irc = socket.socket()
irc = ssl.wrap_socket(irc)

def raw_send(data):
    irc.send((data + "\r\n").encode())


def irc_message(msg):
    raw_send("PRIVMSG " + channel + " :" + msg + "\r\n")

def channel_requests(data):
    print(data)
    for msg in data.split("\r\n"):
        if irc_key + "ping" in msg:
            irc_message("pong")

        if irc_key + "question" in msg:
            msg = msg.split(" ")
            question = msg[2:]
            web_user_id = msg[1]
            for user in db.user.find({"last_active": {"$gte": datetime.utcnow() - timedelta(minutes=2)}}):
                if user["_id"] == web_user_id:
                    db.dialog.insert_one({"uid": web_user_id})
                    irc_message(f"()()Asking {web_user_id}: {question}")
                    return
            irc_message("user has not been online in the last two minutes")


irc.connect((irc_server, irc_port))
raw_send("USER " + irc_nick + " 0 * " + ":" + irc_nick + "\r\n")
raw_send("NICK " + irc_nick + "\r\n")
raw_send("JOIN " + channel + "\r\n")

while True:
    data = irc.recv(4096).decode("utf8")

    print("entering")
    for user in db.user.find({"last_active": {"$gte": datetime.utcnow() - timedelta(minutes=2)}}):
        print("users")
        if not user["mentioned"]:
            irc_message(f"()(){user['_id']} just opened the website()()")
            db.user.update_one({"_id": user["_id"]}, {"mentioned": True})
        for dialog_response in db.dialog_response.find({"uid": user["_id"], "mentioned": False}):
            irc_message(f"(){user['_id']} answered {dialog_response['response']}"            
                        f" to question {dialog_response['question']}")

    if "ING" in data:
        raw_send("PONG")
        continue

    if "PRIVMSG " + channel in data:
        print("found")
        t = threading.Thread(target=channel_requests, args=(channel, data))
        t.daemon = True
        t.start()
        continue