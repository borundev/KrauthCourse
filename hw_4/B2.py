import random, math, pylab
import numpy as np


d=199

x=[0]*d
delta = 0.1
n_trials = 400000
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
print 2 * n_hits / float(n_trials)
    
