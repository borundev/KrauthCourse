import random, math,pylab
import numpy as np
from functools import cache
from tqdm import tqdm

@cache
def psi_n(x,n):
    if n==-1:
        return 0
    elif n==0:
        return 1 / math.pi ** (1 / 4) * math.exp(-x ** 2 / 2)
    else:
        return math.sqrt(2/n)*x*psi_n(x,n-1)-math.sqrt((n-1)/n)*psi_n(x,n-2)


def psi_n_square(x, n):
    return psi_n(x,n)**2
    
beta=5.0
locations=[]
ns=[]
x = 0.0001
delta = 0.5
n=1
for k in tqdm(range(100000)):

    # sample new position for the same energy level
    x_new = x + random.uniform(-delta, delta)
    if random.uniform(0.0, 1.0) <  \
         psi_n_square(x_new,n)/psi_n_square(x,n): 
        x = x_new 
    
    # sample new energy level for the same position
    n_new=n + random.choice([-1,1])
    if n_new >=0 and random.uniform(0.0,1.0) < psi_n_square(x,n_new)/psi_n_square(x,n)*np.exp(-beta*(n_new-n)):
        n=n_new
        
    locations.append(x)
    ns.append(n)
    
xrange=np.arange(-10,10,.1)

pylab.hist(locations,density=True,label='Histogram')
pylab.plot(xrange, np.sqrt(np.tanh(beta/2) / np.pi)*np.exp( - xrange**2 * np.tanh(beta/2) ),label='pi_quant')
 
pylab.plot(xrange, np.sqrt(beta/2/ np.pi)*np.exp( - beta * xrange**2/2 ),label='pi_class')

pylab.xlabel('x')
pylab.ylabel('Probability')
pylab.title('Probability to be at location x for beta='+str(beta))
pylab.legend()
pylab.show()

