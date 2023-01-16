
import rsa
from dataclasses import dataclass, field

def _load_key(filepath: str, kind: str) -> rsa.PublicKey | rsa.PrivateKey | None:
    with open (filepath, 'rb') as pemfile:
        keydata = pemfile.read()
    if kind == 'priv':
        return rsa.PrivateKey.load_pkcs1(keydata)
    elif kind == 'pub':
        return rsa.PublicKey.load_pkcs1(keydata)
    else:
        raise ValueError(f'Key kind must be priv or pub, not {kind}')

@dataclass
class NapsterKeyManager:
    __pub_key : rsa.PublicKey = field(default_factory=lambda: _load_key('./key/napster.pem', 'pub'))
    __priv_key : rsa.PrivateKey = field(default_factory=lambda: _load_key('./key/napster.pem', 'priv'))

    def get_pub_key(self) -> bytes:
        return rsa.PublicKey.save_pkcs1(self.__pub_key)

    def get_pub_key(self, encoding='UTF-8') -> str:
        return rsa.PublicKey.save_pkcs1(self.__pub_key).decode(encoding)
    
    

# if __name__ == '__main__':
#     manager = NapsterKeyManager()
#     print(manager)



    
    
