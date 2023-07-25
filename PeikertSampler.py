from params import Params, SOLMAE_D #same as falcon python code
from fft import mul_fft, Solmae_ifft, fft, ifft #same as falcon python code
from N_sampler import n_sampler #coded by JH
from samplerz import samplerz #same as falcon python code
from os import urandom
#page 14 Algorithm 5
def PeikertSampler(t, Sigma, randombytes=urandom, nu = Params[SOLMAE_D]["smoothing"]):
    rand_vec = n_sampler(randombytes)
    p = mul_fft(Sigma, rand_vec)
    p = Solmae_ifft(p)
    t = ifft(t)
    # x = []
    # for i in range(SOLMAE_D):
    #     x.append(samplerz(t[i]-p[i], Params[SOLMAE_D]["sigma"], nu))
    x = list(map(lambda i: samplerz(t[i]-p[i], Params[SOLMAE_D]["sigma"], nu), list(range(SOLMAE_D))))
    
    return fft(x)

if __name__ == '__main__':
    t = [i for i in range(SOLMAE_D)]
    Sigma = [i for i in range(SOLMAE_D)]
    print(PeikertSampler(t, Sigma))