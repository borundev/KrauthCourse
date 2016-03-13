import random, math,os
import numpy as np
import pylab

def energy(S, N, nbr):
    E = 0.0
    for k in range(N):
        E -=  S[k] * sum(S[nn] for nn in nbr[k])
    return 0.5 * E

L = 128
N = L * L
nbr = {i : ((i // L) * L + (i + 1) % L, (i + L) % N,
            (i // L) * L + (i - 1) % L, (i - L) % N)
                                    for i in range(N)}
T = 2.27
p  = 1.0 - math.exp(-2.0 / T)
nsteps = 1000


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


E = [energy(S, N, nbr)]
for step in range(nsteps):
    print step  
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



f = open(filename, 'w')
for a in S:
   f.write(str(a) + '\n')
f.close()

def x_y(k, L):
    y = k // L
    x = k - y * L
    return x, y

def x_y_inverse(x,y, L):
    return y*L + x






def corr(j):
    c=[]
    for k in range(L):
        x,y=x_y(k,L)
        c.append(S[k]*(S[x_y_inverse(x+j,y,L)]+S[x_y_inverse(x-j,y,L)]+S[x_y_inverse(x,y+j,L)]+S[x_y_inverse(x,y-j,L)])/4.0)
    return np.mean(c)

correlation=[corr(k) for k in range(L)]

pylab.plot(range(L),correlation)
pylab.show()