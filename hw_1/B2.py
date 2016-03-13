import random

n_trials = 2**12

for delta in [.062,.125,.25,.5,1.0,2.0,4.0]:
	x, y = 1.0, 1.0
	n_hits = 0
	accepted=0
	for i in range(n_trials):
    		del_x, del_y = random.uniform(-delta, delta), random.uniform(-delta, delta)
    		if abs(x + del_x) < 1.0 and abs(y + del_y) < 1.0:
        		x, y = x + del_x, y + del_y
			accepted+=1
    		if x**2 + y**2 < 1.0: n_hits += 1
	print str(delta)+":"+ str(accepted / float(n_trials))
