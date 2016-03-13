import random, math,pylab
import numpy as np

def psi_n_square(x, n):
    if n == -1:
        return 0.0
    else:
        psi = [math.exp(-x ** 2 / 2.0) / math.pi ** 0.25]
        psi.append(math.sqrt(2.0) * x * psi[0])
        for k in range(2, n + 1):
            psi.append(math.sqrt(2.0 / k) * x * psi[k - 1] -
                       math.sqrt((k - 1.0) / k) * psi[k - 2])
        return psi[n] ** 2
    
beta=5.0
locations=[]
ns=[]
x = 0.0001
delta = 0.5
n=1
for k in range(100000):
    x_new = x + random.uniform(-delta, delta)
    if random.uniform(0.0, 1.0) <  \
         psi_n_square(x_new,n)/psi_n_square(x,n): 
        x = x_new 
    
    
    n_new=n + random.choice([-1,1])
    if n_new >=0 and random.uniform(0.0,1.0) < psi_n_square(x,n_new)/psi_n_square(x,n)*np.exp(-beta*(n_new-n)):
        n=n_new
        
    locations.append(x)
    ns.append(n)
    
xrange=np.arange(-10,10,.1)

pylab.hist(locations,normed=True,label='Histogram')
pylab.plot(xrange, np.sqrt(np.tanh(beta/2) / np.pi)*np.exp( - xrange**2 * np.tanh(beta/2) ),label='pi_quant')
 
pylab.plot(xrange, np.sqrt(beta/2/ np.pi)*np.exp( - beta * xrange**2/2 ),label='pi_class')

pylab.xlabel('x')
pylab.ylabel('Probability')
pylab.title('Probability to be at location x for beta='+str(beta))
pylab.legend()
pylab.show()

