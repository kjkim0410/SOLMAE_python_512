from keygen import secret_key, public_key, keygen
from fft import fft, ifft, sub, adj_fft, mul_fft, sub_fft, add, mul
from ntt import add_zq, mul_zq
from Crypto.Hash import SHAKE256
from common import q
from rng import ChaCha20
from os import urandom
from Sampler import sampler
from params import SOLMAE_D, Params
from encoding import compress, decompress
HEAD_LEN = 1
SALT_LEN = 40
SEED_LEN = 56


DEBUG = False
DEBUG1 = False


logn = {
    2: 1,
    4: 2,
    8: 3,
    16: 4,
    32: 5,
    64: 6,
    128: 7,
    256: 8,
    512: 9,
    1024: 10
}

def hash_to_point(message, salt):
    """
    Hash a message to a point in Z[x] mod(Phi, q).
    Inspired by the Parse function from NewHope.
    """
    n = SOLMAE_D
    if q > (1 << 16):
        raise ValueError("The modulus is too large")

    k = (1 << 16) // q
    # Create a SHAKE object and hash the salt and message.
    shake = SHAKE256.new()
    shake.update(salt)
    shake.update(message)
    # Output pseudorandom bytes and map them to coefficients.
    hashed = [0 for i in range(n)]
    i = 0
    j = 0
    while i < n:
        # Takes 2 bytes, transform them in a 16 bits integer
        twobytes = shake.read(2)
        elt = (twobytes[0] << 8) + twobytes[1]  # This breaks in Python 2.x
        # Implicit rejection sampling
        if elt < k * q:
            hashed[i] = elt % q
            i += 1
        j += 1
    return hashed

def sign(sk, message= urandom(SOLMAE_D), randombytes=urandom):
    """
    Sign a message. The message MUST be a byte string or byte array.
    Optionally, one can select the source of (pseudo-)randomness used
    (default: urandom).
    """
    #int_header = 0x30 + logn[sk.n]
    #header = int_header.to_bytes(1, "little")
    int_header = 0x30 + logn[SOLMAE_D]
    header = int_header.to_bytes(1, "little")

    salt = randombytes(SALT_LEN)


    if DEBUG:
        print("salt in 40 bytes=",salt)

    if DEBUG:
        print("====================")
        print("message is ", message)
        print("====================")

    hashed = hash_to_point(message, salt)

    c1=[0 for i in range(SOLMAE_D)]
    c2=hashed
    
    if DEBUG1:
        print("=======================")
        print("c1=",c1)
        print("hashed value c2=",c2)
        print("=======================")
    
    c1_fft=fft(c1)
    c2_fft=fft(c2)

    if DEBUG1:
        print("=======================")
        print("after fft c1=",c1_fft)
        print("after fft c2=",c2_fft)
        print("=======================")
    
    # We repeat the signing procedure until we find a signature that is
    # short enough (both the Euclidean norm and the bytelength)
    while(1):
        v0, v1 = sampler(c2_fft, sk, randombytes) #Do not need to send c1_fft # get v0 and v1 in fourier domain(complex value)
        if DEBUG:
            print("=======================")
            print("v0 in fourier domain=",v0)
            print("v1 in fourier domain=",v1)
            print("=======================")
        s1=sub(c1_fft,v0)
        s2=sub(c2_fft,v1)
        if DEBUG:
            print("=======================")
            print("s1=",s1)
            print("=======================")
            print("s2=",s2)
            print("=======================")

            # print("Exiting....")
            # print(exit())

        s1=ifft(s1)
        s2=ifft(s2)

        s1 = [(round(coef) + (q >> 1)) % q - (q >> 1) for coef in s1]
        s2 = [(round(coef) + (q >> 1)) % q - (q >> 1) for coef in s2]

        if DEBUG:
            print("====================")
            print("ifft s1=",s1)
            print("====================")
            print("ifft s2=",s2)
            print("====================")
            # print("Exiting....")
            # print(exit())

        norm_sign = sum(coef**2 for coef in s1)
        norm_sign += sum(coef**2 for coef in s2)
        
        if DEBUG:
            print("norm_sign is ", norm_sign)
            print("====================")

        #Check the Euclidean norm
        if norm_sign <= Params[SOLMAE_D]["sig_bound"]:
            enc_s = compress(s1, Params[SOLMAE_D]["sig_bytelen"]- HEAD_LEN - SALT_LEN)
            # Check that the encoding is valid (sometimes it fails)
            if (enc_s is not False):
                #return header + salt + enc_s
                if DEBUG:
                    print("compressed s1=",enc_s)
                return header+salt+enc_s

def verify(pk, message, signature):
    """
    Verify a signature.
    """
    if DEBUG:
        print("MSG to verify is",message)
        print("verification key is",pk.h)

    # Unpack the salt and the short polynomial s1
    # salt = signature[HEAD_LEN:HEAD_LEN + SALT_LEN]
    # enc_s = signature[HEAD_LEN + SALT_LEN:]

    #check headerbyte is correct or not later
    salt=signature[HEAD_LEN:HEAD_LEN + SALT_LEN]
    enc_s = signature[HEAD_LEN + SALT_LEN:]
    s1 = decompress(enc_s, Params[SOLMAE_D]["sig_bytelen"]- HEAD_LEN - SALT_LEN, SOLMAE_D)
    
    if DEBUG1:
        print("=====================================")
        print("decompressed s1 =",s1)
        print("=====================================")

    # Check that the encoding is valid
    if (s1 is False):
        print("Invalid encoding")
        return False

    # Compute s0 and normalize its coefficients in (-q/2, q/2]
    hashed = hash_to_point(message, salt)
    s2 = add_zq(hashed, mul_zq(s1, pk.h))
    
    s2 = [(coef + (q >> 1)) % q - (q >> 1) for coef in s2]

    if DEBUG1:
        print("hashed in verification =",hashed)
        print("=====================================")
        print("Recentered s2 =",s2)
        print("=====================================")

    # Check that the (s0, s1) is short
    norm_sign = sum(coef**2 for coef in s1)
    norm_sign += sum(coef**2 for coef in s2)
    
    if DEBUG1:
        print("norm_sign in verficiation =",norm_sign)
        print("=====================================")

    if norm_sign > Params[SOLMAE_D]["sig_bound"]:
        print("Squared norm of signature is too large:", norm_sign)
        return False

    # If all checks are passed, accept
    return True
