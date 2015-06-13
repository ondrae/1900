import os
import twilio
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
    resp.say("Welcome to the party line.")
    resp.say("Press 1 to hear a message")
    resp.say("Press 2 to talk to someone")
    resp.say("Press 3 to talk to everyone")
    resp.say("Press 0 to come back to the menu")
 
    return str(resp)
 
if __name__ == "__main__":
    app.run(debug=True)