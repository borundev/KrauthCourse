import random, math

x, y, z = 0.0, 0.0, 0.0
delta = 0.1
n_trials = 400000
n_hits = 0
for i in range(n_trials):
    del_x, del_y, del_z = random.uniform(-delta, delta), random.uniform(-delta, delta),random.uniform(-delta, delta)
    if ((x + del_x)**2 + (y + del_y)**2+(z + del_z)**2 < 1.0):
        x, y,z  = x + del_x, y + del_y, z + del_z
    if x**2 + y**2 + z**2 + random.uniform(-1, 1)**2 < 1.0: n_hits += 1
print 2 * n_hits / float(n_trials)
print 3*math.pi/8