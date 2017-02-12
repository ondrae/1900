#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import twilio.twiml
from twilio.rest import TwilioRestClient
from flask import Flask, request, render_template
import filters

# Flask config
SECRET_KEY = "a secret key"
app = Flask(__name__)
app.secret_key = SECRET_KEY
app.register_blueprint(filters.blueprint)

# Twilio config
account_sid = os.environ["ACCOUNT_SID"]
auth_token = os.environ["AUTH_TOKEN"]
client = TwilioRestClient(account_sid, auth_token)


# ROUTES
@app.route("/", methods=['GET'])
def menu():
    """ Play a menu """
    print "Playing main menu"
    resp = twilio.twiml.Response()
    with resp.gather(numDigits=1, action="/menu_press", method="POST") as gather:
        gather.play("https://s3-us-west-1.amazonaws.com/after-the-tone/900menu.mp3")
    return str(resp)


@app.route("/sms", methods=['GET'])
def sms():
    """ Answer text messages  """
    print "Answering a text message"
    resp = twilio.twiml.Response()
    resp.message("i want to hear the sound of your voice. call me. 💋")
    return str(resp)


@app.route("/menu_press", methods=['POST'])
def menu_press():
    """ What to do when they use the menu """
    digits = request.values.get('Digits', None)
    resp = twilio.twiml.Response()

    if digits not in ["1","2","3","4"]:
        resp.redirect("/", method="GET")
        return str(resp)

    if digits == "1":
        print "1 pressed"
        return privatepartyline(resp)

    if digits == "2":
        print "2 pressed"
        return grouppartyline(resp)

    if digits == "3":
        print "3 pressed"
        return cry(resp)

    if digits == "4":
        print "4 pressed"
        return leaveamessage(resp)


@app.route("/recordings")
def recordings():
    recordings = client.recordings.list()
    return render_template("recordings.html", recordings=recordings)


# Menu options
def privatepartyline(resp):
    # Connect two people in a private partyline
    # Prep response
    d = resp.dial()
    kwargs = {
        "waitUrl" : "https://s3-us-west-1.amazonaws.com/after-the-tone/holdmusicprivatepartyline.mp3",
        "waitMethod" : "GET",
        "maxParticipants" : 2
    }

    # Find which partyline to add caller to
    partylines = client.conferences.list(status="in-progress")

    # If nothing active, start a new line
    if not partylines:
        d.conference("privatepartyline", **kwargs)
        print "privatepartyline"
        return str(resp)

    # else find a privatepartyline with one person waiting
    for partyline in partylines:
        if "privatepartyline" in partyline.friendly_name:
            conference = client.conferences.get(sid=partyline.sid)
            participants = conference.participants.list()
            if len(participants) == 1:
                d.conference(conference.friendly_name, **kwargs)
                print conference.friendly_name
                return str(resp)

    # If still no friendly_name, start a new one
    friendly_name = "privatepartyline" + str(len(partylines))
    d.conference(friendly_name, **kwargs)
    print friendly_name
    return str(resp)


def grouppartyline(resp):
    # The group party line
    # get number of other people
    friendly_name = "grouppartyline"
    conference = client.conferences.list(friendly_name=friendly_name, status="in-progress")
    if conference:
        participants = conference[0].participants.list()
        if participants:
            sentence = "There are " + str(len(participants)) + " others talking on the party line."
            resp.say(sentence, voice="alice", language="en-GB")

    d = resp.dial()
    kwargs = {
        "waitUrl" : "https://s3-us-west-1.amazonaws.com/after-the-tone/holdmusicgrouppartyline.mp3",
        "waitMethod" : "GET",
        "maxParticipants" : 40
    }
    d.conference(friendly_name, **kwargs)
    return str(resp)


def cry(resp):
    # Play a message
    # Any key will return to menu
    with resp.gather(numDigits=1, action="/", method="GET") as gather:
        gather.play("https://s3-us-west-1.amazonaws.com/after-the-tone/crying.mp3")
    resp.redirect("/", method="GET")
    return str(resp)


def leaveamessage(resp):
    # Leave a message
    resp.say("Press any key when done.", voice="alice", language="en-GB")
    resp.redirect("/", method="GET")
    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
