SOLMAE_D = 512

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



# Bytelength of the signing salt and header
HEAD_LEN = 1
SALT_LEN = 320
SEED_LEN = 56

SOLMAE_Q = 12289

# Parameter sets for Falcon:
# - n is the dimension/degree of the cyclotomic ring
# - sigma is the std. dev. of signatures (Gaussians over a lattice)
# - sigmin is a lower bounds on the std. dev. of each Gaussian over Z
# - sigbound is the upper bound on ||s0||^2 + ||s1||^2
# - sig_bytelen is the bytelength of signatures
# need to check parameter's values later
# Params = {
#     # FalconParam(2, 2)
#     2: {
#         "n": 2,
#         "sigma": 144.81253976308423,
#         "sigmin": 1.1165085072329104,
#         "sig_bound": 101498,
#         "sig_bytelen": 44,
#     },
#     # FalconParam(4, 2)
#     4: {
#         "n": 4,
#         "sigma": 146.83798833523608,
#         "sigmin": 1.1321247692325274,
#         "sig_bound": 208714,
#         "sig_bytelen": 47,
#     },
#     # FalconParam(8, 2)
#     8: {
#         "n": 8,
#         "sigma": 148.83587593064718,
#         "sigmin": 1.147528535373367,
#         "sig_bound": 428865,
#         "sig_bytelen": 52,
#     },
#     # FalconParam(16, 4)
#     16: {
#         "n": 16,
#         "sigma": 151.78340713845503,
#         "sigmin": 1.170254078853483,
#         "sig_bound": 892039,
#         "sig_bytelen": 63,
#     },
#     # FalconParam(32, 8)
#     32: {
#         "n": 32,
#         "sigma": 154.6747794602761,
#         "sigmin": 1.1925466358390344,
#         "sig_bound": 1852696,
#         "sig_bytelen": 82,
#     },
#     # FalconParam(64, 16)
#     64: {
#         "n": 64,
#         "sigma": 157.51308555044122,
#         "sigmin": 1.2144300507766141,
#         "sig_bound": 3842630,
#         "sig_bytelen": 122,
#     },
#     # FalconParam(128, 32)
#     128: {
#         "n": 128,
#         "sigma": 160.30114421975344,
#         "sigmin": 1.235926056771981,
#         "sig_bound": 7959734,
#         "sig_bytelen": 200,
#     },
#     # FalconParam(256, 64)
#     256: {
#         "n": 256,
#         "sigma": 163.04153322607107,
#         "sigmin": 1.2570545284063217,
#         "sig_bound": 16468416,
#         "sig_bytelen": 356,
#     },
#     # FalconParam(512, 128)
#     512: {
#         "n": 512,
#         "sigma": 165.7366171829776,
#         "sigmin": 1.2778336969128337,
#         "sig_bound": 34034726,
#         "sig_bytelen": 666,
#     },
#     # FalconParam(1024, 256)
#     1024: {
#         "n": 1024,
#         "sigma": 168.38857144654395,
#         "sigmin": 1.298280334344292,
#         "sig_bound": 70265242,
#         "sig_bytelen": 1280,
#     },
# }

#check compatibility with Solmae C source later
Params = {
    # SolmaeParam(512, 128)
    512: {
        "d": 512,
#        "sigma": 165.7366171829776, #same as falcon need to check
        "sigma": 1.32, #comes from Solmae C source
        "sigmin": 1.2778336969128337, #same as falcon need to check
#        "sig_bound": 34034726, #for falcon
        "sig_bound" : 33870790,
        "sig_bytelen": 666, #same as falcon need to check
        "smoothing" : 1.338,
        "quality" : 1.17,
        "correction" : 0.065,
        "lower_radius": 101.95,
        "upper_radius" : 122.49,
        "signature_width" : 173.54,
        "slack" : 1.04,
    },
    # SolmaeParam(1024, 256)
    1024: {
        "d": 1024,
#        "sigma": 168.38857144654395, #same as falcon need to check
        "sigma": 1.32,
        "sigmin": 1.298280334344292, #same as falcon need to check
#        "sig_bound": 70265242, # for falcon
        "sig_bound" : 134150669,
        "sig_bytelen": 1375, #same as falcon need to check
        "smoothing" : 1.351,
        "quality" : 1.64,
        "correction" : 0.3,
        "lower_radius": 100.85,
        "upper_radius" : 148.54,
        "signature_width" : 245.62,
        "slack" : 1.04,
    },
}

