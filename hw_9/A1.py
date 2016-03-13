import random, math, pylab,os
import numpy as np
os.environ['PATH'] = os.environ['PATH'] + ':/usr/texbin'

from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('text', usetex=True)


def prob(x):
    s1 = np.exp(-(x + 1.2) ** 2 / 0.72)
    s2 = np.exp(-(x - 1.5) ** 2 / 0.08)
    return (s1 + 2.0 * s2) / math.sqrt(2.0 * math.pi)


delta = .001
nsteps = 100000
acc_tot = 0
acc_tmp=0
x = 0.0
x_av = 0.0
xvals=[]
for step in xrange(nsteps):
    xnew = x + random.uniform(-delta, delta)
    if random.uniform(0.0, 1.0) < prob(xnew) / prob(x):
        x = xnew
        acc_tot += 1
        acc_tmp +=1
    if step>0  and step  % 100==0:
        if acc_tmp>60:
            delta = delta*1.1
        elif acc_tmp<40:
            delta= delta/1.1
        acc_tmp=0
    x_av += x
    xvals.append(x)

print 'global acceptance ratio:', acc_tot / float(nsteps)
print '<x> =', x_av / float(nsteps)
x_range = np.linspace(-5,5,500)
print 'Numerical <x>='+ str(np.sum(x_range*prob(x_range))*(x_range[1]-x_range[0]))

pylab.hist(xvals,normed=True,bins=100, label='Simulated Values')
pylab.plot(x_range,prob(x_range),label='Exact Probability Distribution')
pylab.xlabel(r'$x$')
pylab.ylabel(r'$\rho(x)$')
pylab.legend()
pylab.savefig('A1.png')
pylab.clf()
pylab.plot(xvals)
pylab.show()
