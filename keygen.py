# from params import SOLMAE_D, Params
from Pairgen import Pairgen
from ntt import ntt, intt, div_ntt
from ntrugen import ntru_solve
from fft import fft, ifft, add_fft, sub_fft, mul_fft, div_fft, adj_fft, cut_half_fft
from numpy import sqrt
from params import Params, SOLMAE_D
from os import urandom
class secret_key:
    def __init__(self):
        # self.b10 = []
        # self.b11 = []
        # self.b20 = []
        # self.b21 = []
        # self.b20_tild = []
        # self.b21_tild = []
        self.Sigma1 = []
        self.Sigma2 = []
        # self.beta10 = []
        # self.beta11 = []
        # self.beta20 = []
        # self.beta21 = []
        
        self.b10_fft = []
        self.b11_fft = []
        self.b20_fft = []
        self.b21_fft = []
        # self.b20_tild_fft = [] #maybe useless check later
        # self.b21_tild_fft = [] #maybe useless check later
        self.beta10_fft = []
        self.beta11_fft = []
        # self.beta20_fft = []
        self.beta21_fft = []
    def __repr__(self):
        res = "Secretkey"
        res += "\n=====================================\n"
        res += "Sigma1 ="+str(self.Sigma1)
        res += "\n=====================================\n"
        res += "Sigma2 ="+str(self.Sigma2)
        res += "\n=====================================\n"
        res += "b10_fft ="+ str(self.b10_fft)
        res += "\n=====================================\n"
        res += "b11_fft ="+str(self.b11_fft)
        res += "\n=====================================\n"
        res += "b20_fft ="+str(self.b20_fft)
        res += "\n=====================================\n"
        res += "b21_fft ="+str(self.b21_fft)
        res += "\n=====================================\n"
        res += "beta10_fft ="+str(self.beta10_fft)
        res += "\n=====================================\n"
        res += "beta11_fft ="+str(self.beta11_fft)
        res += "\n=====================================\n"
        res += "beta21_fft ="+str(self.beta21_fft)
        res += "\n=====================================\n"
        return res

class public_key:
    def __init__(self):
        self.h = []

    def __repr__(self):
        return "=====================================\n"+"publickey h ="+str(self.h) +"\n=====================================\n"

def keygen(randombytes=urandom):
    sk = secret_key()
    pk = public_key()
    f =[]
    g =[]
    F=[]
    G=[]
    while True:
        f, g = Pairgen(randombytes)
        try:
            f_ntt = ntt(f)
            g_ntt = ntt(g)
            h_ntt = div_ntt(g_ntt, f_ntt)
        except ZeroDivisionError:
            continue

        try:
            F, G = ntru_solve(f, g) # just used ntru_solve from falcon. Not sure if this is appropriate for Solmae
        except ValueError:
            continue

        pk.h = intt(h_ntt)
        break

    eta_sq = Params[SOLMAE_D]["smoothing"]**2
    # eta_sq = 1.7902(from Solmae spec)
    # however etq_sq = 1.7424 in C code. Not sure which is right
    #2023.2.4
    sig_width = Params[SOLMAE_D]["signature_width"]**2
    # In Solmae spec, no squared value described. But, squared value works correctly.
    # 2023.2.4
    eta_sq_fft = [eta_sq for _ in range(SOLMAE_D)]
    sig_width_fft = [sig_width for _ in range(SOLMAE_D)]

    #define beta1
    sk.b10_fft = fft(f)
    sk.b11_fft = fft(g)
    b1_norm = add_fft(mul_fft(adj_fft(sk.b10_fft), sk.b10_fft),mul_fft(adj_fft(sk.b11_fft), sk.b11_fft))
    sk.beta10_fft = div_fft(sk.b10_fft, b1_norm)
    sk.beta11_fft = div_fft(sk.b11_fft, b1_norm)
    beta10 = ifft(sk.beta10_fft)
    beta11 = ifft(sk.beta11_fft)

    #define Sigma1
    sk.Sigma1 = [sqrt(elem) for elem in cut_half_fft(sub_fft(div_fft(sig_width_fft, b1_norm) , eta_sq_fft))]

    #define b2_tild
    sk.b20_fft = fft(F)
    sk.b21_fft = fft(G)
    temp_fft = add_fft(mul_fft(adj_fft(sk.beta10_fft), sk.b20_fft), mul_fft(adj_fft(sk.beta11_fft), sk.b21_fft))
    sk.b20_tild_fft = sub_fft(sk.b20_fft, mul_fft(temp_fft, sk.b10_fft))
    sk.b21_tild_fft = sub_fft(sk.b21_fft, mul_fft(temp_fft, sk.b11_fft))
    
    #define beta2
    b2_tild_norm = add_fft(mul_fft(adj_fft(sk.b20_tild_fft), sk.b20_tild_fft),mul_fft(adj_fft(sk.b21_tild_fft), sk.b21_tild_fft) )
    sk.beta21_fft = div_fft(sk.b21_tild_fft, b2_tild_norm)

    #define Sigma2
    sk.Sigma2 = [sqrt(elem) for elem in cut_half_fft(sub_fft(div_fft(sig_width_fft, b2_tild_norm) , eta_sq_fft))]

    return sk, pk

if __name__ == '__main__':
    for _ in range(10):
        sk, pk = keygen()
        print("h is" ,pk.h)
        print("h_len is ", len(pk.h))
        print("f_fft is ", sk.b10_fft)
        print("f_fft_len is ", len(sk.b10_fft))
        print("g_fft is ", sk.b11_fft)
        print("g_fft_len is ", len(sk.b11_fft))
        print("F_fft is ", sk.b20_fft)
        print("F_fft_len is ", len(sk.b20_fft))
        print("G_fft is ", sk.b21_fft)
        print("G_fft_len is ", len(sk.b21_fft))
        print("beta10_fft is ", sk.beta10_fft)
        print("beta10_fft_len is ", len(sk.beta10_fft))
        print("beta11_fft is ", sk.beta11_fft)
        print("beta11_fft_len is ", len(sk.beta11_fft))
        print("beta21_fft is ", sk.beta21_fft)
        print("beta21_fft_len is ", len(sk.beta21_fft))
        print("Sigma1 is ", sk.Sigma1)
        print("Sigma1_len is ", len(sk.Sigma1))
        print("Sigma2 is ", sk.Sigma2)
        print("Sigma2_len is ", len(sk.Sigma2))

