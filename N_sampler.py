import numpy as np
from rng import ChaCha20
from os import urandom
import matplotlib.pyplot as plt
from params import SOLMAE_D

m_ln2 = 0.693147180559945309417
m_pi = 3.14159265358979323846

def ffsll(word): # find first bit set in word and subtract 1. Program from math library of C source into python
    num = 0
    if word & 0xffffffff == 0:
        num += 32
        word >>= 32
    if word & 0xffff == 0:
        num += 16
        word >>= 16
    if word & 0xff ==0:
        num += 8
        word >>= 8
    if word & 0xf ==0:
        num += 4
        word >>= 4
    if word & 0x3 == 0:
        num += 2
        word >>= 2
    if word & 0x1 == 0:
        num += 1
    return num

def n_sampler(randombytes=urandom):
    coeffs = []

    for i in range(SOLMAE_D//2):
        # put 64bit random numbers in u, v, e.
        u = int.from_bytes(randombytes(8), 'little')
        uf = 2* m_pi *(u & 0x1fffffffffffff) * 2**(-53)
        v = int.from_bytes(randombytes(8), 'little')
        vf = 1/2+ (v & 0x1fffffffffffff)* 2**(-54)
        e_1 = int.from_bytes(randombytes(8), 'little')
        e_2 = int.from_bytes(randombytes(8), 'little')
        # Use constant time macro
        x = 64 + ffsll(e_2)
        y = ffsll(e_1)
        c = ((~e_1)&(e_1 - 1)) >> 63
        geom = (x & (-(c&1)))^(y & (~(-(c&1))))
        vf = np.sqrt(SOLMAE_D*(m_ln2*geom-np.log(vf)))
        # statement above is equivalent to u_rho ~ U(0,1), vf = sqrt(-d*ln(u_rho))
        coeffs.append(vf*np.cos(uf))
        coeffs.append(vf*np.sin(uf))
    return coeffs


if __name__ == '__main__':
    x_list = []
    y_list = []
    for _ in range(20):
        coeffs = n_sampler()
        for i in range(SOLMAE_D//2):
            x = coeffs[2*i]
            y = coeffs[2*i+1]
            x_list.append(x)
            y_list.append(y)

    plt.figure(1)
    plt.plot(x_list,y_list, 'o', markersize=3)
    plt.xlim([-80, 80])
    plt.ylim([-80, 80])
    plt.show()