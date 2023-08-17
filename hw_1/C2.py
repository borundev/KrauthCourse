import random, math

n_trials = 400000
obs=[]
for iter in range(n_trials):
    x, y = random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0)
    if x**2 + y**2 < 1.0:
        obs.append(4.0)
    else:
	    obs.append(0.0)

obs_mean=math.fsum(obs)/n_trials
obs_sq_mean=math.fsum([i**2 for i in obs])/n_trials


print("<Obs>:"+str(obs_mean))
print("<Obs^2>:"+str(obs_sq_mean))
print("Variance:"+str(obs_sq_mean-obs_mean**2))
print("Std Deviation:"+str(math.sqrt(obs_sq_mean-obs_mean**2)))
