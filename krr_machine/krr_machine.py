#!/usr/bin/env python2

import sys
import numpy as np
from copy import deepcopy
from fml.math import cho_solve
from scipy.stats import pearsonr

if __name__ == "__main__":

    ntrain = int(sys.argv[1])
    # if ntrain > 6400:
    #     print "ERROR: N too large!"
    #     exit()

    ntest = 772

    D  = np.load("D.npy")[:ntrain,:ntrain]
    Ds = np.load("D.npy")[:ntrain,-ntest:]

    Y  = np.load("Y.npy")[:ntrain]
    Ys = np.load("Y.npy")[-ntest:]

    offset = np.mean(Y)
    Y -= offset

    sigmas = [0.1 * 2**i for i in range(0,20)]
    llambdas = [10.0**i for i in range(-20,-0)]

    sigmas   = [10.0]
    llambdas = [1e-05]

    minmae = 999999999999999999999.9 

    print D.shape
    print Ds.shape
    print Y.shape
    print Ys.shape

    for sigma in sigmas:
        C = deepcopy(D)
        C = np.exp(C * (-0.5 / sigma**2))

        Ks = np.exp(Ds * (-0.5 / sigma**2))

        for llambda in llambdas:

            K = deepcopy(C)

            for i in range(ntrain):
                K[i,i] += llambda

            alpha = cho_solve(K, Y)

            Y_tilde = np.dot(Ks.transpose(), alpha) + offset

            mae = np.mean(np.abs(Y_tilde - Ys))
            print mae, sigma, llambda,

            if mae < minmae:
                minmae = mae
                print pearsonr(Y_tilde, Ys)

                # ydata = pd.DataFrame(dict({ label1 : (Ys_smd), 
                #                            label2 : (Y_tilde)}))

                # sns.set(style="whitegrid")
                # ax = sns.lmplot(x=label1, y=label2, data=ydata)
                # # ax.set(xlim=[-4, 12], ylim=[-4,12])
                # pyplot.savefig("correlation.png")
                # pyplot.close("all")

            else:
                print
