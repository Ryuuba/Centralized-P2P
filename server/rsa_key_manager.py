import rsa
from dataclasses import dataclass, field

def __load_key(filepath: str, kind: str) -> rsa.PublicKey | rsa.PrivateKey | None:
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
    __dir: str = './key'
    __filename: str = 'napster.pem'
    __pub_key = field(default_factory=__load_key(__dir+__filename, 'pub'))
    __priv_key = field(default_factory=__load_key(__dir+__filename, 'priv'))
    
