from charm.toolbox.pairinggroup import PairingGroup, ZR , G1, pair
from charm.toolbox.hash_module import Hash

# Initialize the pairing group
group = PairingGroup('SS512')

# step 1 
def dc_to_do(sk_k,qk_i):
    # sk_k - private key of DC_k
    # qk_i - public key of DO_p_i

    # Random value selection by DC
    a_k = group.random(ZR)

    # Point computation
    P = group.random(G1)
    t_k = a_k * P

    # Compute the bilinear mapping from private key , public key 
    e_result = group.pair(sk_k,qk_i)

    # Hashing operation
    hash_input = t_k + e_result
    hash_result_k = Hash(hash_input, group)

    # This data will be sent to DO over a public channel
    return (a_k,t_k ,hash_result_k)

# step 3
def do_to_dc(sk_i,qk_k):
    # sk_i - private key of DO_p_i
    # qk_k - public key of DC_k 

    a_i,t_i,hash_result_i=dc_to_do(sk_i,qk_k)
    return (a_i,t_i,hash_result_i)


# step 2 and 4
def correctness(t_k,sigma,sk_i,qk_k):
    # Compute the bilinear mapping from private key , public key 
    e_result = group.pair(sk_i,qk_k)

    # Hashing operation
    hash_input = t_k + e_result
    hash_result = Hash(hash_input, group)

    return sigma==hash_result

# step 5
def common_session_key(id_i,id_k,t_i,t_k,a_i,a_k,hash_result_i,P):
    input1=id_i+id_k+t_i+t_k+a_i*t_k
    hash_result_1=Hash(input1,group)

    input2= id_i+id_k+t_i+t_k+a_k*t_i
    hash_result_2=Hash(input2,group)

    input3=id_i+id_k+t_i+t_k+hash_result_i*a_k*P
    hash_result_3=Hash(input3,Hash)

    if hash_result_1==hash_result_2==hash_result_3:
        return hash_result_3
    return None


import random
# step 6
def select_keyword(word_list):
    # Selecting a random word from the list
    random_word = random.choice(word_list)

    print("Randomly selected word:", random_word)



