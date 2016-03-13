import math, random, pylab
import numpy as np

from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
## for Palatino and other serif fonts use:
#rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)

def levy_harmonic_path(k):
    x = [random.gauss(0.0, 1.0 / math.sqrt(2.0 * math.tanh(k * beta / 2.0)))]
    if k == 2:
        Ups1 = 2.0 / math.tanh(beta)
        Ups2 = 2.0 * x[0] / math.sinh(beta)
        x.append(random.gauss(Ups2 / Ups1, 1.0 / math.sqrt(Ups1)))
    return x[:]

def pi_x(x, beta):
    sigma = 1.0 / math.sqrt(2.0 * math.tanh(beta / 2.0))
    return np.exp(-x ** 2 / (2.0 * sigma ** 2)) / np.sqrt(2.0 * np.pi) / sigma


beta = 2.0
nsteps = 1000000
low = levy_harmonic_path(2)
high = low[:]
data = []
for step in xrange(nsteps):
    k = random.choice([0, 1])
    low[k] = levy_harmonic_path(1)[0]
    high[k] = low[k]
    data.append([low[0],low[1]])
    

data_np=np.array(data)
pylab.hist(data_np[:,0],bins=100,alpha=0.5,normed=True,label='first particle')
pylab.hist(data_np[:,1],bins=100,alpha=0.5,normed=True,label='second particle')
pylab.plot(np.arange(-2,2,.1),pi_x(np.arange(-2,2,.1),beta),label='analytic')
pylab.xlabel(r'$x$')
pylab.ylabel(r'$\pi(x)$')
pylab.title('Distinguishable Particles')
pylab.legend()
pylab.savefig('A1.png')