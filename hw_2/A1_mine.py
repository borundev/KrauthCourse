import random, math
import numpy as np
import pandas as pd

def direct_disks_box(N, sigma):
    condition = False
    while condition == False:
        L = [(random.uniform(sigma, 1.0 - sigma), random.uniform(sigma, 1.0 - sigma))]
        for k in range(1, N):
            a = (random.uniform(sigma, 1.0 - sigma), random.uniform(sigma, 1.0 - sigma))
            min_dist = min(math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) for b in L)
            if min_dist < 2.0 * sigma:
                condition = False
                break
            else:
                L.append(a)
                condition = True
    return L


def direct_disks_box2(N,sigma):
	condition=False
	while condition==False:
		L=sigma+ (1.0 - sigma)*np.random.rand(N,2)
		for i in range(N):
			for j in range(i+1,N):
				diff=np.abs(L[i]-L[j])
				dist=np.sqrt(diff[0]**2 + diff[1]**2)
				if dist < 2.0 * sigma:
					condition=False
					break
				else:
					condition=True
			if condition==False:
				break
	return L



sigma = 0.15
del_xy = 0.05
n_runs = 1000000
conf_a = ((0.30, 0.30), (0.30, 0.70), (0.70, 0.30), (0.70,0.70))
conf_b = ((0.20, 0.20), (0.20, 0.80), (0.75, 0.25), (0.75,0.75))
conf_c = ((0.30, 0.20), (0.30, 0.80), (0.70, 0.20), (0.70,0.70))
configurations = [np.array(conf_a), np.array(conf_b), np.array(conf_c)]
hits = {0: 0, 1: 0, 2: 0}
for run in range(n_runs):
     x_vec = direct_disks_box(4, sigma)
     condition_hit=True
     for j,conf in enumerate(configurations):
	for disk in x_vec:
		if pd.DataFrame([pd.DataFrame(np.abs(disk-conf[i])<np.array([del_xy,del_xy])).all().values[0] for i in range(4)]).any().values[0]:
			condition_hit *=True
		else:
			condition_hit *=False
			break
	if condition_hit:
		hits[j] += 1
for a in hits:
    print a, hits[a]
