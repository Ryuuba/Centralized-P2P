from dataclasses import dataclass, field

@dataclass
class NapsterMsg:
    """
    This class models a Napster message
    """
    __payload_type: dict = field(
        default_factory = lambda: ({
            0x0002: 'login',
            0x0003: 'login ack', 
            0x0010: 'req pub key',
            0x0011: 'public_key',
            0x0064: 'notification',
            0x00C8: 'search',
            0x00C9: 'response',
            0xFFFF: 'error'}
        )
    )
    __max_size = 1024
    length: int = 0
    type: int = 0x0000
    payload: list = field(default_factory= lambda: [])

    def to_bytes(self) -> bytes:
        msg = b''
        msg += self.length.to_bytes()
        msg += self.type.to_bytes()
        msg += ' '.join(self.payload).encode(encoding = 'UTF-8')
        return msg

    def print_type(self) -> str:
        return self.__payload_type[self.type]
    
    def parse(self) -> bool:
        try:
            assert self.__payload_type.get(self.type) is not None
        except AssertionError:
            print(f' Server parser: Invalid type {self.type}, dropping msg')
            return False
        try:
            assert self.type%2 == 0
        except AssertionError:
            print(f' Server parser: Message type is not a request, but a response, dropping msg')
            return False
        # try:
        #     assert len(self.payload) == 4
        # except AssertionError:
        #     print(f' Server parser: Message length {len(self.payload)} does not match with length parameter value {self.length}')
        #     return False
        if self.type == 0x0002:
            return self.__parse_login()
        elif self.type == 0x0064:
            return self.__parse_notification()
        elif self.type == 0x00C8:
            return self.__parse_search()
        
    def __parse_login(self) -> bool:
        try:
            assert len(self.payload) == 4
        except AssertionError:
            print(f' Server parser: Invalid number of fields in login message, received {len(self.payload)}, required 4, dropping msg')
            return False
        try:
            int(self.payload[2])
        except ValueError:
            print(f' Server parser: Port number {self.payload[2]} on login message is not numeric, dropping msg')
            return False
        return True
        
    def __parse_notification(self) -> bool:
        try:
            assert len(self.payload) == 6
        except AssertionError:
            print(f' Server parser: Invalid number of fields in notification message, received {len(self.payload)}, required 6, dropping msg')
            return False
        try:
            assert len(len(self.payload[1])) == 16
        except AssertionError:
            print(f' Server parser: MD5 is a 16-byte field, but only {len(self.payload[1])} are received, dropping msg')
            return False
        try:
            int(self.parse[1], base=16)
        except ValueError:
            print(f' Server parser: MD5 is not a numeric hash value')
            return False
        try:
            int(self.payload[2])
        except ValueError:
            print(f' Server parser: Size is not a numeric value')
        return True

    # TODO: implement this method and test the parse operation
    def __parse_search(self) -> None:
        pass

    def __str__(self) -> str:
        return f'Message length = {self.length} bytes\n'\
            + f'Message type = {self.type:4x} ({self.__payload_type[self.type]})\n'\
            + 'Payload: ' + ' '.join(self.payload)

if __name__ == '__main__':
    msg = NapsterMsg()
    msg.length = 20
    msg.type = 0x0064
    msg.payload = '002000641234567890ABCDEFGHIJ'
    print(msg)