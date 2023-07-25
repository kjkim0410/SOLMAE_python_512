# SOLMAE_python_512

This repository implements the signature scheme, SOLMAE (https://ircs.re.kr/?p=1714).

SOLMAE stands for quantum-**S**ecure alg**O**rithm for **L**ong-term **M**essage **A**uthentication and **E**ncryption

## Content

This repository contains the following files (roughly in order of dependency):

1. [`common.py`](common.py) contains shared functions and constants
1. [`rng.py`](rng.py) implements a ChaCha20-based PRNG(standalone)
1. [`samplerz.py`](samplerz.py) implements a Gaussian sampler over the integers (standalone)
1. [`fft_constants.py`](fft_constants.py) contains precomputed constants used in the FFT
1. [`ntt_constants.py`](ntt_constants.py) contains precomputed constants used in the NTT
1. [`fft.py`](fft.py) implements the FFT over R[x] / (x<sup>n</sup> + 1)
1. [`ntt.py`](ntt.py) implements the NTT over Z<sub>q</sub>[x] / (x<sup>n</sup> + 1)
1. [`ntrugen.py`](ntrugen.py) generate polynomials f,g,F,G in Z[x] / (x<sup>n</sup> + 1) such that f G - g F = q
1. [`params.py`](params.py) contains parameters
1. [`Unifcrown.py`](Unifcrown.py) implements Unifcrown
1. [`Pairgen.py`](Pairgen.py) implements Pairgen
1. [`keygen.py`](keygen.py) implements keygen
1. [`PeikertSampler.py`](PeikertSampler.py) implements PeikertSampler
1. [`N_sampler.py`](N_sampler.py) implements N-sampler
1. [`Sampler.py`](Sampler.py) implements Sample
1. [`sign.py`](sign.py) implements sign and verif
1. [`encoding.py`](encoding.py) implements compress and decompress
1. [`test.py`](test.py) contains how to use code


## How to use

1. Generate a secret key and public key
```
sk = SecretKey()
pk = PublicKey()
sk, pk=keygen()
```

2. Now we can sign messages:
`signature = sign(sk, message)`
Note that the message MUST be a byte array or byte string.

3. We can also verify signatures: `verify(pk, message, signature)`


## Author

* **Kwangjo Kim** (kkj@kaist.ac.kr)
* **Jaehyun Kim** (rlawogus0502@snu.ac.kr)
* **Jueun Jung** (jueun@snu.ac.kr)


## Disclaimer

This is not reference code. The reference code of SOLMAE in C language is on https://kpqc.or.kr/competition.html.
This is work in progress. It is not to be considered secure or suitable for production. This Python script was successfully compiled and verified by Python 3.8.9. for our implementation.
Also, I do not guarantee portability on Python 2.x.
However, this Python code is rather simple, so We hope that it will be helpful to people seeking to implement SOLMAE.

If you find errors or flaw, we will be more than happy if you report them to me at the provided address.

## License

MIT
