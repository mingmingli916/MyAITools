from twilio.rest import Client


class Sender:
    def __init__(self,
                 account_sid="AC27de07df1f83e3975b0914b8c3057fe5",
                 auth_token='7002bf873d8744bf5cd919d07e4acd04',
                 to="+8615101551318",
                 from_="+17029797636"):
        self.to = to
        self.from_ = from_
        self.client = Client(account_sid, auth_token)

    def send(self, msg):
        self.client.messages.create(to=self.to, from_=self.from_, body=msg)
