from pyexpat.errors import messages


class ResponseMessage:
    def __init__(self, message, status):
        self.message = message
        self.status = status

    def __repr__(self):
        return f'<ResponseMessage {self.status}>'


    def create_response_message(self):
        match type(self.message).__name__:
            case 'str' | 'dict':
                return {"message": self.message, "status": self.status}
            case 'list':
                return {"message": [item.to_dict() for item in self.message], "status": self.status}
            case 'User':
                return {"message": self.message.to_dict(), "status": self.status}
            case _:
                return f'invalid type {type(self.message).__name__}', self.status