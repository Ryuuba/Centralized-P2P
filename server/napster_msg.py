from dataclasses import dataclass, field
from napster_key_manager import NapsterKeyManager

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
    payload: list[str] = field(default_factory= lambda: [])

    def get_keyword_list(self) -> str | None:
        pass

    def to_bytes(self) -> bytes:
        """Serializes this message

        Returns:
            bytes: A byte representation of this message
        """
        msg = b''
        msg += f'{self.length:04d}'.encode(encoding = 'UTF-8')
        msg += f'{self.type:04x}'.encode(encoding = 'UTF-8')
        msg += ''.join(self.payload).encode(encoding = 'UTF-8')
        return msg

    def get_type(self) -> str | None:
        """Returns the name of the type corresponding to a message code

        Returns:
            str | None: If the message code is valid, then a str object is return; otherwise, a None object
        """
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
            print(f' Server parser: Public key request message must not have any payload')
            return False
        return True
    
    #TODO process client's RSA pub key
    def __parse_login(self) -> bool:
        try:
            assert len(self.payload) == 4
        except AssertionError:
            print(f' Server parser: Invalid number of fields in login message, received {len(self.payload)}, required 4')
            return False
        try:
            int(self.payload[2])
        except ValueError:
            print(f' Server parser: Port number {self.payload[2]} on login message is not numeric')
            return False
        return True
        
    def __parse_notification(self) -> bool:
        try:
            assert len(self.payload) == 7
        except AssertionError:
            print(f'Server parser:\n Invalid number of fields in notification message,\n received {len(self.payload)},\n required 7: (distro, SHA256, size, version, arch, target, url)')
            return False
        try:
            assert len(self.payload[1]) == 64
        except AssertionError:
            print(f' Server parser: SH256 is a 64 hex char field, but only {len(self.payload[1])} are received')
            return False
        try:
            int(self.payload[1], base=16)
        except ValueError:
            print(f' Server parser: SHA256 is not a numeric hash value')
            return False
        try:
            int(self.payload[2])
        except ValueError:
            print(f' Server parser: Size is not a numeric value')
        return True    

    def __parse_search(self) -> None:
        try:
            assert len(self.payload) == 1
        except AssertionError:
            print(f' Server parser: Search message payload must have only one keyword, actual number of fields equals {len(self.payload)}')
            return False
        return True  

    def __str__(self) -> str:
        msg = f'Message length = {self.length} bytes\n'\
            + f'Message type = {self.type:#0{6}x} ({self.__payload_type[self.type]})\n'\
            + 'Payload: '
        msg += ' '.join(self.payload) if self.payload else 'None'
        return msg

def compose_pub_key_ack(key_manager: NapsterKeyManager) -> NapsterMsg:
    """Returns the message corresponding to a login request

    Returns:
        NapsterMsg: A message containing the server's public rsa key the client must used to encrypt its login messages.
    """
    reply = NapsterMsg()
    reply.type = 0x0011
    reply.payload.append(key_manager.get_pub_key())
    reply.length = len(reply.payload[0])
    return reply

def compose_login_ack(user_email: str) -> NapsterMsg:
    """Returns the message corresponding to a login request

    Returns:
        NapsterMsg: A message that contains the user email that is attempting to log in
    """
    reply = NapsterMsg()
    reply.type = 0x0003
    reply.payload.append(user_email)
    reply.length = len(''.join(reply.payload))
    return reply

def compose_search_response(keyword: list[str]):
    reply = NapsterMsg()
    reply.type = 0x00C9
    # distro (0), version(1), arch(2), size(3), target(4), name(5), ip(6), port(7) 
    distro = keyword[0]
    version = keyword[1]
    arch = keyword[2]
    size = str(keyword[3])
    target = keyword[4]
    name = keyword[5]
    ip = keyword[6]
    port = str(keyword[7])
    space = ' '
    reply.payload.append(distro + space + version + space + arch + space + size + space + 
                         target + space + name + space + ip + space + port)
    reply.length = len(''.join(reply.payload))
    return reply

if __name__ == '__main__':
    msg = NapsterMsg()
    msg.length = 22
    msg.type = 0x0064
    msg.payload = 'This is a 22-byte test'
    print(msg.to_bytes())