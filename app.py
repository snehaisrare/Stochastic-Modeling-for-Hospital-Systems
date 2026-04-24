from flask import Flask, render_template, request, redirect, url_for
import os, io, base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from simulate_birth_death import gillespie_birth_death, sample_trajectory_to_array

app = Flask(__name__)
STATIC_DIR = os.path.join(app.root_path, 'static')
os.makedirs(STATIC_DIR, exist_ok=True)

def plot_history(history, out_path):
    # step plot
    times = [0.0]
    vals = [history[0][1]]
    for (tt, ss) in history[1:]:
        times.append(tt)
        vals.append(vals[-1])
        times.append(tt)
        vals.append(ss)
    plt.figure(figsize=(8,3.5))
    plt.step(times, vals, where='post')
    plt.xlabel('Time')
    plt.ylabel('State (population)')
    plt.title('Sample Birth–Death Trajectory')
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()

def plot_empirical(samples, max_n, analytical, out_path):
    counts, bins = np.histogram(samples, bins=range(max_n+2), density=True)
    centers = (bins[:-1] + bins[1:]) / 2.0
    plt.figure(figsize=(8,3.5))
    plt.bar(centers, counts, width=0.8, alpha=0.6)
    plt.plot(range(len(analytical)), analytical[:len(counts)], marker='o')
    plt.xlabel('State n')
    plt.ylabel('Probability')
    plt.title('Empirical vs Analytical')
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()
    return counts

def analytical_geom(lam, mu, max_n):
    rho = lam/mu
    if rho >= 1.0:
        # return truncated heavy tail normalized
        arr = [1.0/(max_n+1)]*(max_n+1)
        return arr
    pi0 = 1.0 - rho
    return [pi0*(rho**n) for n in range(max_n+1)]

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run():
    # read parameters
    lam = float(request.form.get('lam', 2.0))
    mu = float(request.form.get('mu', 3.0))
    t_max = float(request.form.get('tmax', 10.0))
    n_sims = int(request.form.get('nsims', 500))
    max_n = int(request.form.get('maxn', 40))
    x0 = int(request.form.get('x0', 0))

    # single history
    history = gillespie_birth_death(lambda n: lam, lambda n: mu if n>0 else 0.0, x0, t_max)
    traj_path = os.path.join(STATIC_DIR, 'trajectory.png')
    plot_history(history, traj_path)

    # many sims
    samples = []
    for _ in range(n_sims):
        h = gillespie_birth_death(lambda n: lam, lambda n: mu if n>0 else 0.0, x0, t_max)
        s = sample_trajectory_to_array(h, [t_max])[0]
        samples.append(s)
    analytical = analytical_geom(lam, mu, max_n)
    emp_counts = plot_empirical(samples, max_n, analytical, os.path.join(STATIC_DIR, 'emp_vs_analytical.png'))

    # prepare dataframe for display
    df = pd.DataFrame({
        'state': range(len(emp_counts)),
        'empirical_prob': emp_counts,
        'analytical_prob': analytical[:len(emp_counts)]
    })
    csv_path = os.path.join(STATIC_DIR, 'distribution_comparison.csv')
    df.to_csv(csv_path, index=False)

    return render_template('result.html', traj_img='static/trajectory.png', emp_img='static/emp_vs_analytical.png', csv_file='static/distribution_comparison.csv', lam=lam, mu=mu, t_max=t_max, n_sims=n_sims)

if __name__ == '__main__':
    # allow running with: python app.py
    app.run(host='0.0.0.0', port=5000, debug=True)
