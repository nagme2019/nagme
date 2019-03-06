# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client


# Your Account Sid and Auth Token from twilio.com/console
account_sid = 'ACf46f7868cc321426fc41dbbe0ea4676e'
auth_token = 'f091327b9ce1bb5900b28edc8bb416b3'
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body="Join Earth's mightiest heroes. Like Kevin Bacon.",  # top nag text
                     from_='',  # insert twilio number
                     to=''  # insert phone number
                 )

print(message.sid)