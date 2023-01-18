#from Crypto.PublicKey import RSA
#import Crypto
from dataclasses import dataclass
import sys
import os
import chilkat

@dataclass

class createKeys:

    rsa = chilkat.CkRsa()
    success = rsa.GenerateKey(1024)
    
    def generarKey(self) -> None:
        
        if (self.success != True):
            print(self.rsa.lastErrorText())
            sys.exit()

        pubKey = self.rsa.ExportPublicKeyObj()
        privKey = self.rsa.ExportPrivateKeyObj()

        pubKey64 = pubKey.getEncoded(True,"base64")
        privKey64 = privKey.getPkcs1ENC("base64")

        if os.path.isfile('./key/napster1.pem'):
            print("Ya existe la llave")
        else:
            f = open('napster1.pem','w')
            f.write("-----BEGIN RSA PUBLIC KEY-----\n")
            f.write(pubKey64)
            f.write("\n-----END RSA PUBLIC KEY-----\n")
            f.write("\n-----BEGIN RSA PRIVATE KEY-----\n")
            f.write(privKey64)
            f.write("\n-----END RSA PRIVATE KEY-----\n")
            f.close()