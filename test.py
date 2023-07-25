from sign import sign, verify
from keygen import secret_key, public_key, keygen
from os import urandom
from params import SOLMAE_D

iterations=3
round=0
for i in range(iterations):
    round+=1
    print("number of round=",round)
    sk=secret_key()
    pk=public_key()
    sk, pk = keygen()
    message=urandom(SOLMAE_D)
    signature = sign(sk, message)
    print(verify(pk, message, signature))
