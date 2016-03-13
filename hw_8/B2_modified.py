import random, math,os
import numpy as np
import pylab

def energy(S, N, nbr):
    E = 0.0
    for k in range(N):
        E -=  S[k] * sum(S[nn] for nn in nbr[k])
    return 0.5 * E

L = 2**3
N = L * L
nbr = {i : ((i // L) * L + (i + 1) % L, (i + L) % N,
            (i // L) * L + (i - 1) % L, (i - L) % N)
                                    for i in range(N)}

nsteps = 5000

Ts=np.linspace(1,4,100)
Cs=[]

S = [random.choice([1, -1]) for k in range(N)]

for T in Ts:
    print 'T='+str(T)
    p  = 1.0 - math.exp(-2.0 / T)





    E = [energy(S, N, nbr)]
    for step in range(nsteps):
        k = random.randint(0, N - 1)
        Pocket, Cluster = [k], [k]
        while Pocket != []:
            j = Pocket.pop()
            for l in nbr[j]:
                if S[l] == S[j] and l not in Cluster \
                       and random.uniform(0.0, 1.0) < p:
                    Pocket.append(l)
                    Cluster.append(l)
        for j in Cluster:
            S[j] *= -1
        E.append(energy(S, N, nbr))


    E_np=np.array(E)

    Cs.append(E_np.var() / N / T ** 2)
    
pylab.plot(Ts,np.array(Cs))
pylab.show()
np.savez('SpecificHeat_N='+str(N),Ts,np.array(Cs))


