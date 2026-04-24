import math, random
from typing import Callable, List, Tuple

def gillespie_birth_death(lambda_fn: Callable[[int], float],
                          mu_fn: Callable[[int], float],
                          x0: int,
                          t_max: float,
                          rng=None) -> List[Tuple[float,int]]:
    if rng is None:
        rng = random.random
    t = 0.0
    x = int(x0)
    history = [(t,x)]
    while t < t_max:
        lam = lambda_fn(x)
        mu = mu_fn(x)
        total_rate = lam + mu
        if total_rate <= 0:
            break
        r = random.random()
        tau = -math.log(r) / total_rate
        t += tau
        if t > t_max:
            break
        r2 = random.random() * total_rate
        if r2 < lam:
            x = x + 1
        else:
            x = max(0, x - 1)
        history.append((t, x))
    return history

def sample_trajectory_to_array(history, t_points):
    res = []
    idx = 0
    current_state = history[0][1]
    for tp in t_points:
        while idx + 1 < len(history) and history[idx+1][0] <= tp:
            idx += 1
            current_state = history[idx][1]
        res.append(current_state)
    return res
