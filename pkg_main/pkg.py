# from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2, GT, pair
# from charm.schemes.pkenc import p
from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2, pair
from charm.core.engine.util import objectToBytes, bytesToObject

# Initialize the pairing group
group = PairingGroup('SS512')

# Step 1: Choose the elliptic curve parameters
a = group.random(ZR)
b = group.random(ZR)
curve = {'a': a, 'b': b}
q = group.order()
# print(q)

# Step 2: Choose the cyclic groups G1 and G2
# G1 = group.random(G1)
# G2 = group.random(G2)
# G1 is additive cyclic group
# G2 is multiplicative cyclic group

# Step 3: Choose generators and define the bilinear map
P = group.random(G1)
P1 = group.random(G1)

# Define the bilinear map
def e(a, b):
    return pair(a, b)

# Step 4: Define hash functions
def H0(input_str):
    return group.hash(input_str, G1)

def H1(input_str):
    return group.hash(input_str, ZR)

# Step 5: Generate the master key pair
s = group.random(ZR)
print(type(s))
print(type(P))
P0 = s * P

# Step 6: Publish public parameters
public_parameters = {
    'q': q,
    'G1': G1,
    'G2': G2,
    'P': P,
    'P1': P1,
    'e': e,
    'H0': H0,
    'H1': H1,
    'P0': P0,
}

# The public_parameters dictionary can be used for cryptographic operations

# Example usage of the bilinear map:
# use public parameters
A = group.random(G1)
B = group.random(G1)
result = public_parameters['e'](A, B)
print(result)
# Example usage of hash functions:
message = "Hello, Charm-Crypto!"
hash_result = public_parameters['H0'](message)
print("Hash of the message:", hash_result)

print('Public Parameters')
print(public_parameters)
