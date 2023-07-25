import numpy as np
from params import SOLMAE_D, Params, SOLMAE_Q
from Unifcrown import Unifcrown
from os import urandom
from fft import fft , ifft

m_pi = 3.14159265358979323846
count = 0

def Pairgen(randombytes=urandom):
    global count 
    R_min = Params[SOLMAE_D]["lower_radius"]
    R_max = Params[SOLMAE_D]["upper_radius"]
    while True:
        flag = True
        count+=1
        f_fft = [0 for _ in range(SOLMAE_D)]
        g_fft = [0 for _ in range(SOLMAE_D)]

        for i in range(SOLMAE_D//2):
            x, y = Unifcrown(R_min, R_max)
            u_1 = int.from_bytes(randombytes(8), 'little')
            theta_x = 2* m_pi *(u_1 & 0x1fffffffffffff) * 2**(-53)
            u_2 = int.from_bytes(randombytes(8), 'little')
            theta_y = 2* m_pi *(u_2 & 0x1fffffffffffff) * 2**(-53)
            # multiplied 2pi before this line
            x_re = x*np.cos(theta_x)
            x_im = x*np.sin(theta_x)
            y_re = y*np.cos(theta_y)
            y_im = y*np.sin(theta_y)
            f_fft[i] = complex(x_re, x_im)
            f_fft[i + SOLMAE_D//2] = complex(x_re, -x_im)
            g_fft[i] = complex(y_re, y_im)
            g_fft[i+SOLMAE_D//2] = complex(y_re, -y_im)

        f = list(map(lambda n: round(n), ifft(f_fft)))
        g = list(map(lambda n: round(n), ifft(g_fft)))
        res_f_fft = fft(f)
        res_g_fft = fft(g)
        for i in range(SOLMAE_D//2):
            norm_sq = res_f_fft[i].real**2 + res_f_fft[i].imag**2 + res_g_fft[i].real**2 + res_g_fft[i].imag**2
            if norm_sq < SOLMAE_Q/Params[SOLMAE_D]["quality"]**2 or norm_sq > SOLMAE_Q*Params[SOLMAE_D]["quality"]**2:
                # 8977 16822
                flag = False
                continue
        if flag:
            return f, g

if __name__ == '__main__':
    
    for _ in range(100):
        count = 0
        f, g = Pairgen()
        print("count is ", count)
        print(f[0], g[0])
