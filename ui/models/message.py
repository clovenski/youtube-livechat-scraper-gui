class Message:
    def __init__(self, timestamp, type, user, amount, message):
        self.timestamp = timestamp
        self.type = type
        self.user = user
        self.amount = amount
        self.message = message

    def to_json(self):
        return {
            "timestamp": self.timestamp,
            "type": self.type,
            "user": self.user,
            "amount": self.amount,
            "message": self.message,
        }
