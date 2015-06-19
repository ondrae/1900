import os
import twilio.twiml
from flask import Flask, request, session

# Flask config
app = Flask(__name__)

@app.route("/", methods=['GET'])
def menu():
    """ Play a menu"""
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


if __name__ == "__main__":
    app.run(debug=True)