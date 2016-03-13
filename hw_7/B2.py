import random, math, numpy, sys, os

import numpy as np

os.environ['PATH'] = os.environ['PATH'] + ':/usr/texbin'

from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
## for Palatino and other serif fonts use:
#rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)

def levy_harmonic_path_3d(k):
    x0 = tuple([random.gauss(0.0, 1.0 / math.sqrt(2.0 *
                math.tanh(k * beta / 2.0))) for d in range(3)])
    x = [x0]
    for j in range(1, k):
        Upsilon_1 = 1.0 / math.tanh(beta) + 1.0 / \
                          math.tanh((k - j) * beta)
        Upsilon_2 = [x[j - 1][d] / math.sinh(beta) + x[0][d] /
                     math.sinh((k - j) * beta) for d in range(3)]
        x_mean = [Upsilon_2[d] / Upsilon_1 for d in range(3)]
        sigma = 1.0 / math.sqrt(Upsilon_1)
        dummy = [random.gauss(x_mean[d], sigma) for d in range(3)]
        x.append(tuple(dummy))
    return x

def rho_harm_3d(x, xp):
    Upsilon_1 = sum((x[d] + xp[d]) ** 2 / 4.0 *
                    math.tanh(beta / 2.0) for d in range(3))
    Upsilon_2 = sum((x[d] - xp[d]) ** 2 / 4.0 /
                    math.tanh(beta / 2.0) for d in range(3))
    return math.exp(- Upsilon_1 - Upsilon_2)


N = 512
T_star = .8
beta = 1.0 / (T_star * N ** (1.0 / 3.0))
cycle_min=10


filename = 'data_boson_configuration_N='+str(N)+'.txt'

# read in from file if possible otherwise create initial conditions

positions = {}
if os.path.isfile(filename):
    f = open(filename, 'r')
    for line in f:
        a = line.split()
        positions[tuple([float(a[0]), float(a[1]), float(a[2])])] = \
               tuple([float(a[3]), float(a[4]), float(a[5])])
    f.close()
    if len(positions) != N:
        sys.exit('ERROR in the input file.')
    print 'Starting from file', filename
else:
    for k in range(N):
        a = levy_harmonic_path_3d(1)
        positions[a[0]] = a[0]
    print 'Starting from a new configuration'





hist1_data=[]
hist2_data=[]


# Monte Carlo loop
nsteps = 100000
for step in range(nsteps):
    # move 1: resample one permutation cycle
    boson_a = random.choice(positions.keys())
    hist1_data.append(boson_a[0])
    perm_cycle = []
    while True:
        perm_cycle.append(boson_a)
        boson_b = positions.pop(boson_a)
        if boson_b == perm_cycle[0]:
            break
        else:
           boson_a = boson_b
    k = len(perm_cycle)
    
    if k>cycle_min:
        print k
        hist2_data.append(boson_a[0])
    perm_cycle = levy_harmonic_path_3d(k)
    positions[perm_cycle[-1]] = perm_cycle[0]
    for k in range(len(perm_cycle) - 1):
        positions[perm_cycle[k]] = perm_cycle[k + 1]
    # move 2: exchange
    a_1 = random.choice(positions.keys())
    b_1 = positions.pop(a_1)
    a_2 = random.choice(positions.keys())
    b_2 = positions.pop(a_2)
    weight_new = rho_harm_3d(a_1, b_2) * rho_harm_3d(a_2, b_1)
    weight_old = rho_harm_3d(a_1, b_1) * rho_harm_3d(a_2, b_2)
    if random.uniform(0.0, 1.0) < weight_new / weight_old:
        positions[a_1] = b_2
        positions[a_2] = b_1
    else:
        positions[a_1] = b_1
        positions[a_2] = b_2
#for boson in positions.keys():
#    print boson, positions[boson]
    
    
    


f = open(filename, 'w')
for a in positions:
   b = positions[a]
   f.write(str(a[0]) + ' ' + str(a[1]) + ' ' + str(a[2]) + ' ' +
           str(b[0]) + ' ' + str(b[1]) + ' ' + str(b[2]) + '\n')
f.close()

#print hist1_data
#print hist2_data

import pylab, mpl_toolkits.mplot3d

binwidth=.04
pylab.hist(hist1_data,bins=np.arange(min(hist1_data), max(hist1_data) + binwidth, binwidth),alpha=.5,normed=True,label='All bosons')
if hist2_data:
    pylab.hist(hist2_data,bins=np.arange(min(hist2_data), max(hist2_data) + binwidth, binwidth),alpha=.5,normed=True,label='Bosons on $>$'+str(cycle_min)+' long cycles')
pylab.plot(np.arange(-3,3,.1),np.exp(-np.arange(-3,3,.1)**2)/np.sqrt(np.pi),label=r'Ground state probability $\psi_0(x)^2$')
pylab.xlim(-3.0, 3.0)
pylab.ylabel('Probability')
pylab.xlabel(r'$x')
pylab.title(r'Bose-Einstein condensation')
pylab.legend()
pylab.savefig('B2.png')
