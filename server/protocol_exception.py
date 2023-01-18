class NotificationException(Exception):
    """Exception raised when a client does not follow the napster protocol

    Attributes:
        message (str): The protocol error message (default = Client {} attempts to notify content without logging in previously)
    """    
    def __init__(self, client_ip: str, message="""Client {} attempts to notify content without logging in previously""") -> None:
        self.message = message.format(client_ip)
        super().__init__(self.message)

class UnregisteredUserException(Exception):
    """Exception raised when a user_id is not registered in the Napster database

    Attributes:
        message (str): The protocol error message (default = User {} is unregistered)
    """    
    def __init__(self, user_id: str, message="""User {} is unregistered""") -> None:
        self.message = message.format(user_id)
        super().__init__(self.message)