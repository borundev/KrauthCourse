import math, random, pylab,os
import numpy as np

os.environ['PATH'] = os.environ['PATH'] + ':/usr/texbin'

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

def rho_harm_1d(x, xp, beta):
    Upsilon_1 = (x + xp) ** 2 / 4.0 * math.tanh(beta / 2.0)
    Upsilon_2 = (x - xp) ** 2 / 4.0 / math.tanh(beta / 2.0)
    return math.exp(- Upsilon_1 - Upsilon_2)


def z(beta):
    return 1.0 / (1.0 - math.exp(- beta))




def pi_two_bosons(x, beta):
    pi_x_1 = math.sqrt(math.tanh(beta / 2.0)) / math.sqrt(math.pi) *\
             np.exp(-x ** 2 * math.tanh(beta / 2.0))
    pi_x_2 = math.sqrt(math.tanh(beta)) / math.sqrt(math.pi) *\
             np.exp(-x ** 2 * math.tanh(beta))
    weight_1 = z(beta) ** 2 / (z(beta) ** 2 + z(2.0 * beta))
    weight_2 = z(2.0 * beta) / (z(beta) ** 2 + z(2.0 * beta))
    pi_x = pi_x_1 * weight_1 + pi_x_2 * weight_2
    return pi_x

nsteps = 1000
list_beta=[.1,.5,1,1.5,2,2.5,3,3.5,4,4.5,5]
prob_two_cycles=[]
prob_one_cycle=[]
for beta in list_beta:
    number_one_cycle=0
    number_two_cycles=0
    low = levy_harmonic_path(2)
    high = low[:]
    data = []
    for step in xrange(nsteps):
        # move 1
        if low[0] == high[0]:
            k = random.choice([0, 1])
            low[k] = levy_harmonic_path(1)[0]
            high[k] = low[k]
        else:
            low[0], low[1] = levy_harmonic_path(2)
            high[1] = low[0]
            high[0] = low[1]
        data.append([low[0],low[1]])
        if low[0]==high[0]:
            number_two_cycles +=1
        else:
            number_one_cycle +=1
        #data += low[:]
        # move 2
        weight_old = (rho_harm_1d(low[0], high[0], beta) *
                      rho_harm_1d(low[1], high[1], beta))
        weight_new = (rho_harm_1d(low[0], high[1], beta) *
                      rho_harm_1d(low[1], high[0], beta))
        if random.uniform(0.0, 1.0) < weight_new / weight_old:
            high[0], high[1] = high[1], high[0]
    prob_one_cycle.append(number_one_cycle*1.0/nsteps)
    prob_two_cycles.append(number_two_cycles*1.0/nsteps)



fract_two_cycles = [z(beta) ** 2 / (z(beta) ** 2 + z(2.0 * beta)) for beta in list_beta]
fract_one_cycle = [z(2.0 * beta) / (z(beta) ** 2 + z(2.0 * beta)) for beta in list_beta]

pylab.scatter(list_beta,prob_two_cycles,label='Frac Two-cycles Simulation',c='r')
pylab.scatter(list_beta,fract_two_cycles,label='Frac Two-cycles Analytic',c='g')
pylab.scatter(list_beta,prob_one_cycle,label='Prob One-cycle Simulation',c='b')
pylab.scatter(list_beta,fract_one_cycle,label='Frac One-cycle Analytic',c='y')

pylab.xlabel(r'$\beta$')
pylab.ylabel('Prob of cycles')
pylab.title(r'Indistinguishable Particles: Fractions of one/two cycles')
pylab.legend()
pylab.savefig('A2_2.png')