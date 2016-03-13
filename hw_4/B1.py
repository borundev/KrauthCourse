import random, math, pylab
import numpy as np


d=20

x=[0]*d
delta = 0.1
n_trials = 40000
n_hits = 0

radii=[]

for i in range(n_trials):
    # map an anonymous function to square elements of x and sum
    old_radius_square=sum(map(lambda foo: foo**2,x))
    k=random.randint(0,d-1)
    x_old_k=x[k]
    x_new_k = x_old_k + random.uniform(-delta, delta)
    new_radius_square = old_radius_square + x_new_k ** 2 - x_old_k ** 2
    if new_radius_square<1:
        x[k]=x_new_k
    radii.append(math.sqrt(old_radius_square))
    
pylab.hist(radii,normed=True)
pylab.plot(np.arange(0,1,.01),20*np.arange(0,1,.01)**19)
pylab.title("d=20")
pylab.ylabel("PDF of points at radius r")
pylab.xlabel("r")
pylab.show()