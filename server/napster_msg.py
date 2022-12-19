from dataclasses import dataclass, field

@dataclass
class NapsterMsg:
    """
    This class models a Napster message
    """
    __payload_type: dict = field(
        default_factory = lambda: ({
            0x0002: 'login', 
            0x0064: 'notification',
            0x00C8: 'search',
            0x00C9: 'response'}
        )
    )
    length: int = 0
    type: int = 0x0000
    payload: str = ''

    def print_type(self) -> str:
        return self.__payload_type[self.type]

    def __str__(self) -> str:
        return f'Message length = {self.length} bytes\n'\
            + f'Message type = {self.type} ({self.__payload_type[self.type]})\n'\
            + 'Payload: ' + self.payload

if __name__ == '__main__':
    msg = NapsterMsg()
    msg.length = 20
    msg.type = 0x0064
    msg.payload = '002000641234567890ABCDEFGHIJ'
    print(msg)