import random, math, pylab
import numpy as np


dmax=200

Qs={}

def Q(dP1):
    d=dP1-1
    


    x=[0]*d
    delta = 0.1
    n_trials = 40000
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


def V_sph(d,Qs):
    if d==1: return 2
    return Qs[d]*V_sph(d-1,Qs)

def V_sph_analytical(dim):
    return math.pi ** (dim / 2.0) / math.gamma(dim / 2.0 + 1.0)


for i in range(2,dmax+1):
    print i
    Qs[i]=Q(i)
    
#print "Volume of 4-sphere is " +str(V_sph(4,Qs))
#print "Volume of 200-sphere is " +str(V_sph(200,Qs))


Volumes=[V_sph(i,Qs) for i in range(2,dmax+1)]
Volumes_Analytical=[V_sph_analytical(i) for i in range(2,dmax+1)]
pylab.yscale('log')
pylab.plot(range(2,dmax+1),Volumes, label='Numerical')
pylab.plot(range(2,dmax+1),Volumes_Analytical,  label='Analytical')
pylab.xlabel('dimensions')
pylab.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,ncol=2, mode="expand", borderaxespad=0.)

pylab.show()
