#Name : Paruchuri Chaitanya
#course : CSE 6331   Cloud Computing
#NO: 1000790255
from Crypto.Cipher import AES
from Crypto import Random
import random, struct, hashlib
import sys,os.path
import gntp.notifier
from settings import aespasskey
from settings import APP_KEY,APP_SECRET,ACCESS_TYPE
class Encrypt:
    def __init__(self):
        pass
    
    def encryptFile(self, in_filename, out_filename=None, chunksize=64*1024):
        print("Encrypting: " + in_filename)
	gntp.notifier.mini("Encryption in process")

        
        key = hashlib.sha256(aespasskey).digest()
        
        if not out_filename:
	    in_newfile = in_filename.replace('upload', 'tempenc')
            out_filename = os.path.join(in_newfile + '.enc')
	    print out_filename

        iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
        encryptor = AES.new(key, AES.MODE_CBC, iv)
        filesize = os.path.getsize(in_filename)
        with open(in_filename, 'rb') as infile:
            with open(out_filename, 'wb') as outfile:
                outfile.write(struct.pack('<Q', filesize))
                outfile.write(iv)

                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk) == 0:
                        break
                    elif len(chunk) % 16 != 0:
                        chunk += ' ' * (16 - len(chunk) % 16)

                    outfile.write(encryptor.encrypt(chunk))
        
        print("Encryption finished.")
	gntp.notifier.mini("Encryption Finished")

                    
    def decryptFile(self, data, out_filename=None, chunksize=24*1024):
        in_filename = data
        key = hashlib.sha256(aespasskey).digest()
        
        if not out_filename:
            out_filename = os.path.splitext(in_filename)[0]

        with open(in_filename, 'rb') as infile:
            origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
            iv = infile.read(16)
            decryptor = AES.new(key, AES.MODE_CBC, iv)

            with open(out_filename, 'wb') as outfile:
                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk) == 0:
                        break
                    outfile.write(decryptor.decrypt(chunk))

                outfile.truncate(origsize)
        
