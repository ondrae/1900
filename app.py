import os
import random
from datetime import date
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

@app.route("/", methods=['GET'])
def menu():
    """ Play a menu """
    resp = twilio.twiml.Response()
    with resp.gather(numDigits=1, action="/menu_press", method="POST") as gather:
        gather.say("Welcome to the party line.",voice="alice",language="en-GB")
        gather.say("Press 1 to hear a message",voice="alice",language="en-GB")
        gather.say("Press 2 to talk to someone",voice="alice",language="en-GB")
        gather.say("Press 3 to talk to everyone",voice="alice",language="en-GB")
        gather.say("Press 0 to come back to the menu",voice="alice",language="en-GB")
 
    return str(resp)


@app.route("/menu_press", methods=['POST'])
def menu_press():
    """ What to do when they use the menu """
    digits = request.values.get('Digits', None)
    resp = twilio.twiml.Response()

    if digits == "1":
        resp.play("https://s3-us-west-1.amazonaws.com/after-the-tone/Memo.mp3")
        return str(resp)

    if digits == "2":
        # Get a list of callers from today
        callers = []
        for call in client.calls.list(started_after=date.today()):
            if call.from_ not in callers:
                callers.append(call.from_)

        # Call a random one
        random_caller = random.choice(callers)
        print random_caller
        resp.say("Connecting you to a random.",voice="alice",language="en-GB")
        resp.dial(random_caller)
        return str(resp)


if __name__ == "__main__":
    app.run(debug=True)