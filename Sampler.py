from fft import mul_fft, adj_fft, neg, sub_fft, add_fft, ifft
from PeikertSampler import PeikertSampler
from params import SOLMAE_D, Params
from os import urandom
# programmed from Solmae C code the difference is in C code, beta1, beta2 is already conjugate
def sampler(c2_fft, sk, randombytes=urandom):

    nyu = Params[SOLMAE_D]["smoothing"]
    #c1 = [0]*SOLMAE_D # c1 is always zero vector with degree SOLMAE_D
    # first loop
    z2 = PeikertSampler(mul_fft(adj_fft(sk.beta21_fft), c2_fft), sk.Sigma2, randombytes, nyu)
    v0 = mul_fft(z2, sk.b20_fft)
    v1 = mul_fft(z2, sk.b21_fft)
    temp_c1 = neg(v0)
    temp_c2 = sub_fft(c2_fft, v1)
    
    #second loop
    mu1 = add_fft(mul_fft(adj_fft(sk.beta10_fft), temp_c1), mul_fft(adj_fft(sk.beta11_fft), temp_c2))
    z1 = PeikertSampler(mu1, sk.Sigma1, randombytes, nyu)
    v0 = add_fft(v0, mul_fft(z1, sk.b10_fft))
    v1 = add_fft(v1, mul_fft(z1, sk.b11_fft))

    return v0, v1

if __name__ == '__main__':
    v0, v1 = sampler()
