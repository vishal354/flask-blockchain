# BCT IMDS - Extract

from charm.toolbox.pairinggroup import PairingGroup
from charm.schemes.ibenc.ibenc_bf01 import IBE_BonehFranklin

# Initialize the pairing group
group = PairingGroup('SS512')

# Setup the Boneh-Franklin IBE scheme
ibenc = IBE_BonehFranklin(group)
master_public_key, master_secret_key=None,None

def key_pair():
    global master_public_key
    global master_secret_key
    # Setup the master secret key
    (master_public_key, master_secret_key) = ibenc.setup()
    return master_public_key, master_secret_key

def generate_user_private_key(email):
    key_pair()
    private_key = ibenc.extract( master_secret_key, email)
    return private_key

def encrypt_message(message,email):
    if type(message)!=bytes:
        message = memoryview(message.encode('utf-8')).tobytes()
    ciphertext=ibenc.encrypt(master_public_key, email, message)
    return ciphertext

def decrypt_message(private_key, ciphertext):
    decrypted_message = ibenc.decrypt(master_public_key, private_key, ciphertext)
    return decrypted_message.decode()

# email="acb@jkl.com"
# k=generate_user_private_key(email)
# message = "Hello, this is a secret message!"
# print(decrypt_message(k,encrypt_message(message,email)))