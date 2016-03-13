import random, math, pylab
import numpy as np

L = 32
N = L * L
nbr = {i : ((i // L) * L + (i + 1) % L, (i + L) % N,
            (i // L) * L + (i - 1) % L, (i - L) % N) \
                                    for i in range(N)}

nruns=10
T = 2.4
beta = 1.0 / T
t_coups=[]
for run in range(nruns):
    S0 = np.array([1] * N)
    S1 = np.array([-1] * N)
    step = 0
    while True:
        step += 1
        k = random.randint(0, N - 1)
        Upsilon = random.uniform(0.0, 1.0)
        h = sum(S0[nn] for nn in nbr[k])
        S0[k] = -1
        if Upsilon < 1.0 / (1.0 + math.exp(-2.0 * beta * h)):
            S0[k] = 1
        h = sum(S1[nn] for nn in nbr[k])
        S1[k] = -1
        if Upsilon < 1.0 / (1.0 + math.exp(-2.0 * beta * h)):
            S1[k] = 1
        n_diff = np.sum(np.abs(S0-S1))
        if n_diff == 0:
            t_coup = 1.0*step / N
            t_coups.append(t_coup)
            break
print np.mean(t_coups)