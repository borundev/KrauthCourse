import random, math,os
import numpy as np
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
T = 2.27
p  = 1.0 - math.exp(-2.0 / T)
nsteps = 1000*L*L


filename = 'data_local_'+ str(L) + '_' + str(T) + '.txt'
if os.path.isfile(filename):
    f = open(filename, 'r')
    S = []
    for line in f:
        S.append(int(line))
    f.close()
    print 'Starting from file', filename
else:
    S = [random.choice([1, -1]) for k in range(N)]
    print 'Starting from a random configuration'

S = [ 1 for k in range(N)]

print energy(S,N,nbr)

for step in range(100*L*L):
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



E = []
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
print 'mean energy per spin:', sum(E) / float(len(E) * N)


E_np=np.array(E)

print 'specific heat cv('+str(N)+','+str(T)+')='+str(E_np.var() / N / T ** 2)

#f = open(filename, 'w')
#for a in S:
#   f.write(str(a) + '\n')
#f.close()
