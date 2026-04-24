from simulate_birth_death import gillespie_birth_death, sample_trajectory_to_array
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

lam = 2.0
mu = 3.0
t_max = 10.0
x0 = 0
n_sims = 500
max_n = 40

outdir = os.path.join(os.path.dirname(__file__), 'static')
# single history
hist = gillespie_birth_death(lambda n: lam, lambda n: mu if n>0 else 0.0, x0, t_max)
# plot trajectory
times = [0.0]
vals = [hist[0][1]]
for (tt, ss) in hist[1:]:
    times.append(tt); vals.append(vals[-1]); times.append(tt); vals.append(ss)
plt.figure(figsize=(8,3.5))
plt.step(times, vals, where='post')
plt.xlabel('Time'); plt.ylabel('State'); plt.title('Sample trajectory')
plt.tight_layout()
plt.savefig(os.path.join(outdir, 'trajectory.png')); plt.close()

# many sims
samples = []
for _ in range(n_sims):
    h = gillespie_birth_death(lambda n: lam, lambda n: mu if n>0 else 0.0, x0, t_max)
    s = sample_trajectory_to_array(h, [t_max])[0]
    samples.append(s)
counts, bins = np.histogram(samples, bins=range(max_n+2), density=True)
centers = (bins[:-1]+bins[1:])/2.0
plt.figure(figsize=(8,3.5))
plt.bar(centers, counts, width=0.8, alpha=0.6)
rho = lam/mu
if rho < 1.0:
    pi0 = 1.0 - rho
    analytical = [pi0*(rho**n) for n in range(max_n+1)]
else:
    analytical = [1.0/(max_n+1)]*(max_n+1)
plt.plot(range(len(analytical)), analytical[:len(counts)], marker='o')
plt.xlabel('State n'); plt.ylabel('Probability'); plt.title('Empirical vs Analytical')
plt.tight_layout()
plt.savefig(os.path.join(outdir, 'emp_vs_analytical.png')); plt.close()

df = pd.DataFrame({'state': range(len(counts)), 'empirical_prob': counts, 'analytical_prob': analytical[:len(counts)]})
df.to_csv(os.path.join(outdir, 'distribution_comparison.csv'), index=False)
print('demo images created')
