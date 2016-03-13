import random, math, pylab


def gauss_cut():
    while True:
        x = random.gauss(0.0, 1.0)
        if abs(x) <= 1.0:
            return x

alpha = 0.5
nsamples = 1000000
samples_x = []
samples_y = []
for sample in xrange(nsamples):
    while True:
        
        ##### Changed code to sample x,y from gauss_cut
        #x = random.uniform(-1.0, 1.0)
        #y = random.uniform(-1.0, 1.0)
        x,y=[gauss_cut() for i in range(2)]
        
        ##### Changed code to accept with a new probability which acts together with the sampling to get the correct distribution
        #p = math.exp(-0.5 * (x ** 2 + y ** 2) - alpha * (x ** 4 + y ** 4))
        p = math.exp(- alpha * (x ** 4 + y ** 4))
        if random.uniform(0.0, 1.0) < p:
            break
    samples_x.append(x)
    samples_y.append(y)

pylab.hexbin(samples_x, samples_y, gridsize=50, bins=1000)
pylab.axis([-1.0, 1.0, -1.0, 1.0])
cb = pylab.colorbar()
pylab.xlabel('x')
pylab.ylabel('y')
pylab.title('A1_2')
pylab.savefig('plot_A1_2.png')
pylab.show()
