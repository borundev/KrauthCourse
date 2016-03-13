import math, numpy,pylab

# Free off-diagonal density matrix
def rho_free(x, xp, beta):
    return (math.exp(-(x - xp) ** 2 / (2.0 * beta)) /
            math.sqrt(2.0 * math.pi * beta))

# Harmonic density matrix in the Trotter approximation (returns the full matrix)
def rho_harmonic_trotter(grid, beta):
    return numpy.array([[rho_free(x, xp, beta) * \
                         numpy.exp(-0.5 * beta * 0.5 * (x ** 2 + xp ** 2)) \
                         for x in grid] for xp in grid])

def V(x,cubic,quartic):
    return  x ** 2 / 2.0 + cubic * x ** 3 + quartic * x ** 4

def rho_anharmonic_trotter(grid, beta,cubic, quartic):
    return numpy.array([[rho_free(x, xp, beta) * \
                         numpy.exp(-0.5 * beta * (V(x,cubic,quartic)+V(xp,cubic,quartic))) \
                         for x in grid] for xp in grid])


x_max = 5.0                              # the x range is [-x_max,+x_max]
nx = 100
dx = 2.0 * x_max / (nx - 1)
x = [i * dx for i in range(-(nx - 1) / 2, nx / 2 + 1)]
beta_tmp = 2.0 ** (-6)                   # initial value of beta (power of 2)
beta     = 2.0 ** 2                      # actual value of beta (power of 2)


cubic_g=-1.0
quartic_g=1.0

rho = rho_anharmonic_trotter(x, beta_tmp,cubic_g,quartic_g)  # density matrix at initial beta


while beta_tmp < beta:
    rho = numpy.dot(rho, rho)
    rho *= dx
    beta_tmp *= 2.0
    print 'beta: %s -> %s' % (beta_tmp / 2.0, beta_tmp)
    
Z = sum(rho[j, j] for j in range(nx + 1)) * dx
pi_of_x = [rho[j, j] / Z for j in range(nx + 1)]
f = open('data_anharm_matrixsquaring_beta' + str(beta) + '.dat', 'w')
for j in range(nx + 1):
    f.write(str(x[j]) + ' ' + str(rho[j, j] / Z) + '\n')
f.close()

xrange=numpy.array(x)
pylab.plot(x,pi_of_x,label='anharmonic')
pylab.plot(xrange, numpy.sqrt(numpy.tanh(beta/2) / numpy.pi)*numpy.exp( - xrange**2 * numpy.tanh(beta/2) ),label='harmonic')
pylab.xlabel('x')
pylab.ylabel('Probability')
pylab.title('Probability vs location for anharmonic with quartic=-cubic=1.0')
pylab.legend()
pylab.show()