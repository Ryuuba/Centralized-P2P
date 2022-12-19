from dataclasses import dataclass, field

__payload_type: dict = {
        0x0002: 'login', 
        0x0064: 'notification',
        0x00C8: 'search',
        0x00C9: 'response'
    }

@dataclass
class NapsterMsg:
    """
    This class models a Napster message
    """
    length: int = 0
    type: int = 0x0000
    payload: str = ''

    def print_type(self) -> str:
        return __payload_type[self.type]

    def __str__(self) -> str:
        return str(self.length) + ' ' + str(self.type) + ' ' + self.payload