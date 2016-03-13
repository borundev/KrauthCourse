import math, random, pylab

def rho_free(x, y, beta):    # free off-diagonal density matrix
    return math.exp(-(x - y) ** 2 / (2.0 * beta)) 

def V(x,cubic,quartic):
    return  x ** 2 / 2.0 + cubic * x ** 3 + quartic * x ** 4

def read_file(filename):
    list_x = []
    list_y = []
    with open(filename) as f:
        for line in f:
            x, y = line.split()
            list_x.append(float(x))
            list_y.append(float(y))
    f.close()
    return list_x, list_y

beta = 4.0
N = 16                                            # number of slices
dtau = beta / N
delta = 1.0                                       # maximum displacement on one slice
n_steps = 1000000                                 # number of Monte Carlo steps
x = [0.0] * N                                     # initial path

x0_hist=[]


cubic_g=-1.0
quartic_g=1.0

for step in range(n_steps):
    k = random.randint(0, N - 1)                  # random slice
    knext, kprev = (k + 1) % N, (k - 1) % N       # next/previous slices
    x_new = x[k] + random.uniform(-delta, delta)  # new position at slice k

    old_weight  = (rho_free(x[knext], x[k], dtau) *
                   rho_free(x[k], x[kprev], dtau) *
                   math.exp(-dtau * V(x[k],cubic_g,quartic_g)))
  
    new_weight  = (rho_free(x[knext], x_new, dtau) *
                   rho_free(x_new, x[kprev], dtau) *
                   math.exp(-dtau * V(x_new,cubic_g,quartic_g)))

    if random.uniform(0.0, 1.0) < new_weight / old_weight:
        x[k] = x_new
    if step % 10==0: x0_hist.append(x[0])
    
pylab.hist(x0_hist,normed=True,label='Markov')
pylab.xlim(-2.0, 2.0)
x_list,y_list=read_file('data_anharm_matrixsquaring_beta4.0.dat')
pylab.plot(x_list,y_list,label='Matrix Squaring')
pylab.xlabel('x')
pylab.ylabel('Probability')
pylab.legend()
pylab.title('Comparing matrix-squaring with Markov for anharmonic: cubic='+str(cubic_g)+', quartic='+str(quartic_g))
pylab.show()
