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
            0x0010: 'pubkey req',
            0x0011: 'pubkey ack',
            0x0064: 'notification',
            0x0066: 'notification end',
            0x00C8: 'search',
            0x00C9: 'response',
            0xFFFF: 'error'}
        )
    )
    __max_size = 1024
    length: int = 0
    type: int = 0x0000
    payload: list = field(default_factory= lambda: [])

    def to_bytes(self) -> bytes | None:
        msg = b''
        msg += f'{self.length:04d}'.encode(encoding = 'UTF-8')
        msg += f'{self.type:04x}'.encode(encoding = 'UTF-8')
        msg += ''.join(self.payload).encode(encoding = 'UTF-8')
        return msg

    def get_type(self) -> str | None:
        try:
            return self.__payload_type[self.type]
        except:
            None
    
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
        if self.type == 0x0002:
            return self.__parse_login()
        elif self.type == 0x0010:
            return self.__parse_pubkey_req()
        elif self.type == 0x0064:
            return self.__parse_notification()
        elif self.type == 0x0066:
            return self.__parse_notification_end()
        elif self.type == 0x00C8:
            return self.__parse_search()

    def __parse_pubkey_req(self) -> bool:
        try:
            assert len(self.payload) == 0
        except AssertionError:
            print(f' Server parser: Public key request message must not have any payload, dropping msg')
            return False
        return True
        
    def __parse_login(self) -> bool:
        try:
            assert len(self.payload) == 5
        except AssertionError:
            print(f' Server parser: Invalid number of fields in login message, received {len(self.payload)}, required 5, dropping msg')
            return False
        try:
            int(self.payload[2])
        except ValueError:
            print(f' Server parser: Port number {self.payload[2]} on login message is not numeric, dropping msg')
            return False
        try:
            assert len(self.payload[4]) == 128
        except AssertionError:
            print(f' Public key length does not match 128 bytes, dropping msg')
            return False
        return True
        
    def __parse_notification(self) -> bool:
        try:
            assert len(self.payload) == 6
        except AssertionError:
            print(f' Server parser: Invalid number of fields in notification message, received {len(self.payload)}, required 6, dropping msg')
            return False
        try:
            assert len(len(self.payload[1])) == 32
        except AssertionError:
            print(f' Server parser: SH256 is a 32-bytes field, but only {len(self.payload[1])} are received, dropping msg')
            return False
        try:
            int(self.parse[1], base=16)
        except ValueError:
            print(f' Server parser: SHA256 is not a numeric hash value')
            return False
        try:
            int(self.payload[2])
        except ValueError:
            print(f' Server parser: Size is not a numeric value')
        return True

    def __parse_notification_end(self) -> bool:
        try:
            assert len(self.payload) == 0
        except AssertionError:
            print(f' Server parser: Notification end message must not have any payload, dropping msg')
            return False
        return True        

    def __parse_search(self) -> None:
        try:
            assert len(self.payload) >= 2 and len(self.payload) < 5
        except AssertionError:
            print(f' Server parser: Search message payload must have between two and four fields, actual number of fields equals {len(self.payload)}, dropping message')
            return False
        try:
            int(self.payload[1], base=10)
        except ValueError:
            print(f' Server parser: max result field is not numeric, dropping message')
            return False
        return True  

    def __str__(self) -> str:
        return f'Message length = {self.length} bytes\n'\
            + f'Message type = {self.type:4x} ({self.__payload_type[self.type]})\n'\
            + 'Payload: ' + ' '.join(self.payload)

if __name__ == '__main__':
    msg = NapsterMsg()
    msg.length = 22
    msg.type = 0x0064
    msg.payload = 'This is a 22-byte test'
    print(msg.to_bytes())