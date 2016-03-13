import random, math,pylab
import numpy as np

def psi_0_sq(x):
    return (1/ math.pi**(1.0/2))*math.exp( - x**2 )

locations=[]
x = 0.0
delta = 0.5
for k in range(100000):
    x_new = x + random.uniform(-delta, delta)
    if random.uniform(0.0, 1.0) <  \
         psi_0_sq(x_new)/psi_0_sq(x): 
        x = x_new 
    locations.append(x)



pylab.hist(locations,normed=True,label='Histogram')
pylab.plot(np.arange(-10,10,.1),np.exp(-np.arange(-10,10,.1)**2)/(math.pi**(1/2.0)),label='Analytical')
pylab.xlabel('x')
pylab.ylabel('Probability')
pylab.legend()
pylab.show()

