import math, numpy,pylab

# Free off-diagonal density matrix
def rho_free(x, xp, beta):
    return (math.exp(-(x - xp) ** 2 / (2.0 * beta)) /
            math.sqrt(2.0 * math.pi * beta))



def V(x,cubic,quartic):
    return  x ** 2 / 2.0 + cubic * x ** 3 + quartic * x ** 4

def rho_anharmonic_trotter(grid, beta,cubic, quartic):
    return numpy.array([[rho_free(x, xp, beta) * \
                         numpy.exp(-0.5 * beta * (V(x,cubic,quartic)+V(xp,cubic,quartic))) \
                         for x in grid] for xp in grid])


def Energy_pert(n, cubic, quartic):
    return n + 0.5 - 15.0 / 4.0 * cubic **2 * (n ** 2 + n + 11.0 / 30.0) \
         + 3.0 / 2.0 * quartic * (n ** 2 + n + 1.0 / 2.0)

def Z_pert(cubic, quartic, beta, n_max):
    Z = sum(math.exp(-beta * Energy_pert(n, cubic, quartic)) for n in range(n_max + 1))
    return Z


x_max = 8.0                              # the x range is [-x_max,+x_max]
nx = 250
dx = 2.0 * x_max / (nx - 1)
x = [i * dx for i in range(-(nx - 1) / 2, nx / 2 + 1)]

beta     = 2.0                      # actual value of beta (power of 2)



n_max=10



for s in [0.001,0.01,0.1,0.2,0.3,0.4,0.5]:
    cubic_g=-s
    quartic_g=s
    beta_tmp = 2.0 ** (-6)              # initial value of beta (power of 2)
    
    rho = rho_anharmonic_trotter(x, beta_tmp,cubic_g,quartic_g)  # density matrix at initial beta


    while beta_tmp < beta:
        rho = numpy.dot(rho, rho)
        rho *= dx
        beta_tmp *= 2.0
    
    Z = sum(rho[j, j] for j in range(nx + 1)) * dx
    Z_p=Z_pert(cubic_g, quartic_g, beta, n_max)
    print 'quartic=-cubic='+str(s)+': Z_{pert}='+str(Z_p)+', Z='+str(Z)


