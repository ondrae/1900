import os
import twilio.twiml
from twilio.rest import TwilioRestClient
from flask import Flask, request

# Flask config
SECRET_KEY = "a secret key"
app = Flask(__name__)
app.secret_key = SECRET_KEY

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


def privatepartyline(resp):
    # Connect two people in a private partyline
    # Get list of current partylines
    partylines = client.conferences.list(status="in-progress")

    # grouppartyline is the bigun
    if "grouppartyline" in partylines:
        partylines.remove("grouppartyline")

    # If there arent any, make a new one
    if not partylines:
        print "Making new partyline"
        new_partyline = "partyline1"
        d = resp.dial()
        d.conference(new_partyline)
        return str(resp)

    # Look in newest partyline for someone waiting
    else:
        newest_partyline = partylines.pop()
        newest_partyline_name = newest_partyline.friendly_name
        conference = client.conferences.list(friendly_name=newest_partyline_name)
        participants = conference[0].participants.list()
        if len(participants) == 1:
            d = resp.dial()
            d.conference(newest_partyline_name)
            return str(resp)

        # If they are all paired up, make a new room
        else:
            new_partyline_name = "partyline" + str(len(partylines) + 1)
            d = resp.dial()
            d.conference(new_partyline_name)
            return str(resp)


def grouppartyline(resp):
    # The group party line
    # Can hold up to 40 people
    resp.say("Welcome to the party line.",voice="alice",language="en-GB")
    conference = client.conferences.list(friendly_name="grouppartyline")
    if conference:
        participants = conference[0].participants.list()
        num_participants = str(len(participants))
        sentence = "There are " + num_participants + " talking on the party line."
        resp.say(sentence, voice="alice", language="en-GB")
    d = resp.dial()
    d.conference("grouppartyline")
    return str(resp)


def cry(resp):
    # Play a message
    # Any key will return to menu
    with resp.gather(numDigits=1, action="/", method="GET") as gather:
        gather.play("https://s3-us-west-1.amazonaws.com/after-the-tone/crying.mp3")
    resp.redirect("/", method="GET")
    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)