import random, math, pylab
import numpy as np


dmax=200

Qs={}

def Q(dP1, n_trials):
    d=dP1-1
    


    x=[0]*d
    delta = 0.1
    n_hits = 0


    for i in range(n_trials):
        # map an anonymous function to square elements of x and sum
        old_radius_square=sum(map(lambda foo: foo**2,x))
        k=random.randint(0,d-1)
        x_old_k=x[k]
        x_new_k = x_old_k + random.uniform(-delta, delta)
        new_radius_square = old_radius_square + x_new_k ** 2 - x_old_k ** 2
        if new_radius_square<1:
            x[k]=x_new_k
            radius_squared=new_radius_square
        else:
            radius_squared=old_radius_square
        if radius_squared + random.uniform(-1, 1)**2 < 1.0: n_hits += 1

    return 2 * n_hits / float(n_trials)


def V_sph(d,n_trials):
    if d==1: return 2
    return Q(d,n_trials)*V_sph(d-1,n_trials)

def V_sph_analytical(dim):
    return math.pi ** (dim / 2.0) / math.gamma(dim / 2.0 + 1.0)


print "n_trials | <V_sph(20)> | V_sph(20) (exact) | error | difference"
for n_trials in [10**i for i in range(6)]:
    vals=np.array([V_sph(20,n_trials) for i in range(10)])
    print str(n_trials)+" | "+str(vals.mean())+" | "+str(V_sph_analytical(20))+" | "+str(vals.std())+" | "+ str(vals.mean()-V_sph_analytical(20))