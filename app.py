import os
import twilio.twiml
from flask import Flask

# Flask config
app = Flask(__name__)

# Twilio config
# account_sid = os.environ["ACCOUNT_SID"]
# auth_token  = os.environ["AUTH_TOKEN"]
# client = twilio.TwilioRestClient(account_sid, auth_token)

 
@app.route("/", methods=['GET'])
def menu():
    """ Play a menu"""
    resp = twilio.twiml.Response()
    resp.say("Welcome to the party line.",voice="alice",language="en-GB")
    resp.say("Press 1 to hear a message",voice="alice",language="en-GB")
    resp.say("Press 2 to talk to someone",voice="alice",language="en-GB")
    resp.say("Press 3 to talk to everyone",voice="alice",language="en-GB")
    resp.say("Press 0 to come back to the menu",voice="alice",language="en-GB")
 
    return str(resp)
 
if __name__ == "__main__":
    app.run(debug=True)