import pylab

def show_conf(L, sigma, title, fname):
    pylab.axes()
    for [x, y] in L:
        for ix in range(-1, 1):
            for iy in range(-1, 1):
                cir = pylab.Circle((x + ix, y + iy), radius=sigma,  fc='r')
                print x+ix,y+iy
                pylab.gca().add_patch(cir)
    pylab.axis('scaled')
    pylab.title(title)
    #pylab.axis([-3.0, 3, -3.0, 3])
    pylab.axis([0.0, 1.0, 0.0, 1.0])
    #pylab.plot([0, 0], [0, 1], 'k-', lw=2)
    #pylab.plot([0, 1], [1, 1], 'k-', lw=2)
    #pylab.plot([1, 1], [1, 0], 'k-', lw=2)
    #pylab.plot([1, 0], [0,0], 'k-', lw=2)
    pylab.savefig(fname)
    pylab.show()
    pylab.close()

L = [[0.9, 0.9]]
sigma = 0.4
show_conf(L, sigma, 'test graph', 'one_disk.png')