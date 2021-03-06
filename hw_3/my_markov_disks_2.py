import random,math, pylab, os, sys, cmath
import numpy as np



def show_conf(L, sigma, title="tmp graph", fname="tmp.png"):
    pylab.axes()
    for [x, y] in L:
        for ix in range(-1, 2):
            for iy in range(-1, 2):
                cir = pylab.Circle((x + ix, y + iy), radius=sigma,  fc='r')
                pylab.gca().add_patch(cir)
    pylab.axis('scaled')
    pylab.title(title)
    pylab.axis([0.0, 1.0, 0.0, 1.0])
    pylab.savefig(fname)
    pylab.show()
    pylab.close()

def dist(x,y):
    d_x = abs(x[0] - y[0]) % 1.0
    d_x = min(d_x, 1.0 - d_x)
    d_y = abs(x[1] - y[1]) % 1.0
    d_y = min(d_y, 1.0 - d_y)
    return  math.sqrt(d_x**2 + d_y**2)


def delx_dely(x, y):
    d_x = (x[0] - y[0]) % 1.0
    if d_x > 0.5: d_x -= 1.0
    d_y = (x[1] - y[1]) % 1.0
    if d_y > 0.5: d_y -= 1.0
    return d_x, d_y

def Psi_6(L, sigma):
    sum_vector = 0j
    for i in range(N):
        vector  = 0j
        n_neighbor = 0
        for j in range(N):
            if dist(L[i], L[j]) < 2.8 * sigma and i != j:
                n_neighbor += 1
                dx, dy = delx_dely(L[j], L[i])
                angle = cmath.phase(complex(dx, dy))
                vector += cmath.exp(6.0j * angle)
        if n_neighbor > 0:
            vector /= n_neighbor
        sum_vector += vector
    return sum_vector / float(N)


N=64


eta=.72
sigma_sq= eta/N/math.pi

sigma = math.sqrt(sigma_sq)

N_sqrt=int(math.sqrt(N))

delxy=1.0/(2*N_sqrt)


if delxy < sigma:
    print "density too high, can't fit"
    sys.exit(1)

filename = 'disk_configuration_N%i_eta%.2f.txt' % (N, eta)
if os.path.isfile(filename):
    f = open(filename, 'r')
    L = []
    for line in f:
        a, b = line.split()
        L.append([float(a), float(b)])
    f.close()
    print 'starting from file', filename
else:
    L = [[delxy + i * 2* delxy, delxy + j * 2* delxy] for i in range(int(math.sqrt(N))) for j in range(int(math.sqrt(N)))]
    #L[0][0] = 3.3

    f = open(filename, 'w')
    for a in L:
       f.write(str(a[0]) + ' ' + str(a[1]) + '\n')  
    f.close()







eta=.72
sigma_sq= eta/N/math.pi

sigma = math.sqrt(sigma_sq)

etas=np.arange(.72,0,-.02)
psis=[]

delta = 0.3* sigma
n_steps = 10000
for i,eta in enumerate(etas):
    sigma_sq= eta/N/math.pi
    sigma = math.sqrt(sigma_sq)
    delta = 0.3* sigma
    
    psis_total=0
    
    for steps in range(n_steps):
        a = random.choice(L)
        b = [a[0] + random.uniform(-delta, delta), a[1] + random.uniform(-delta, delta)]
    
        min_dist=min(dist(b,c) for c in L if c!=a)
    
        if not min_dist < 2.0 * sigma:
            b[0] = b[0] % 1
            b[1] = b[1] % 1
            a[:] = b

        if steps % 100 ==0:
            psis_total+=cmath.polar(Psi_6(L, sigma))[0]
    psis.append(1.0*psis_total/n_steps)
    
print psis
pylab.axes()
pylab.plot(etas,psis)
pylab.title("Order parameter plotted against density")
pylab.xlabel("density")
pylab.ylabel("order parameter")
pylab.show()

