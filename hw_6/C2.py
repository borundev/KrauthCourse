import math, random, pylab
import numpy as np

#def rho_free(x, y, beta):
#    return math.exp(-(x - y) ** 2 / (2.0 * beta))

def V(x,cubic,quartic):
    return  x ** 2 / 2.0 + cubic * x ** 3 + quartic * x ** 4


def V_anharm(x,cubic,quartic):
    return  cubic * x ** 3 + quartic * x ** 4


def levy_free_path(xstart, xend, dtau, N):
    x = [xstart]
    for k in range(1, N):
        dtau_prime = (N - k) * dtau
        x_mean = (dtau_prime * x[k - 1] + dtau * xend) / \
                 (dtau + dtau_prime)
        sigma = math.sqrt(1.0 / (1.0 / dtau + 1.0 / dtau_prime))
        x.append(random.gauss(x_mean, sigma))
    return x

def levy_harmonic_path(xstart, xend, dtau, N):
    x = [xstart]
    for k in range(1, N):
        dtau_prime = (N - k) * dtau
        Ups1 = 1.0 / math.tanh(dtau) + \
               1.0 / math.tanh(dtau_prime)
        Ups2 = x[k - 1] / math.sinh(dtau) + \
               xend / math.sinh(dtau_prime)
        x.append(random.gauss(Ups2 / Ups1, \
               1.0 / math.sqrt(Ups1)))
    return x


beta = 20.0
N = 100
dtau = beta / N
#delta = 1.0
n_steps = 400000
x = [0.1] * N
data = []
Ncut = int(N/10.0)
g_cubic=-1.0
g_quartic=1.0

accepted=0


for step in range(n_steps):
    #k = random.randint(0, N - 1)
    #knext, kprev = (k + 1) % N, (k - 1) % N
    #x_new = x[k] + random.uniform(-delta, delta)
    #old_weight  = (rho_free(x[knext], x[k], dtau) *
    #               rho_free(x[k], x[kprev], dtau) *
    #               math.exp(-0.5 * dtau * x[k] ** 2))
    #new_weight  = (rho_free(x[knext], x_new, dtau) *
    #               rho_free(x_new, x[kprev], dtau) *
    #               math.exp(-0.5 * dtau * x_new ** 2))
    #if random.uniform(0.0, 1.0) < new_weight / old_weight:
    #    x[k] = x_new
    
   
    #x_new = levy_free_path(x[0], x[Ncut], dtau, Ncut) + x[Ncut:]
    x_new = levy_harmonic_path(x[0], x[Ncut], dtau, Ncut) + x[Ncut:]
    
    Trotter_weight_old = math.exp(sum(-V_anharm(a, g_cubic, g_quartic) * dtau for a in x))
    Trotter_weight_new = math.exp(sum(-V_anharm(a, g_cubic, g_quartic) * dtau for a in x_new))
    
    if random.uniform(0.0, 1.0) < Trotter_weight_new/Trotter_weight_old:
        x=x_new[:]
        x = x[1:] + x[:1]
        accepted+=1
    
    if step % N == 0:
        k = random.randint(0, N - 1)
        data.append(x[k])
    

print 'acceptance rate='+str(1.0*accepted/n_steps)
np.save('x_positions_C2',x)



pylab.plot(x,np.arange(0,beta,dtau))
pylab.xlabel('$x$')
pylab.ylabel('Imaginary Time')
pylab.title('Path Sample for C2')
pylab.savefig('x_positions_C2.png')
pylab.clf()

pylab.hist(data, normed=True, bins=100, label='QMC')
#list_x = [0.1 * a for a in range (-30, 31)]
#list_y = [math.sqrt(math.tanh(beta / 2.0)) / math.sqrt(math.pi) * \
#          math.exp(-x ** 2 * math.tanh(beta / 2.0)) for x in list_x]
#pylab.plot(list_x, list_y, label='analytic')
pylab.legend()
pylab.xlabel('$x$')
pylab.ylabel('$\\pi(x)$ (normalized)')
pylab.title('anharmonic_path C2 (beta=%s, N=%i)' % (beta, N))
#pylab.xlim(-2, 2)
pylab.savefig('plot_C2_beta%s_levy.png' % beta)
pylab.show()
