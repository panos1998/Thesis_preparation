from typing import Tuple
import math


def normal_approximation_to_binomial(n: int, p: float) -> Tuple[float, float]:
    mu = p * n
    sigma = math.sqrt(p * (1 - p) * n)
    return mu, sigma


from lesson5 import normal_cdf


normal_probability_below = normal_cdf


def normal_probability_above(lo: float,
                             mu: float =0,
                             sigma: float = 1) -> float:
    return 1-normal_cdf(lo, mu, sigma)


def normal_probability_between(lo: float, hi: float, mu: float = 0, sigma: float = 1):
    return normal_cdf(hi, mu, sigma) - normal_cdf(lo, mu, sigma)


def normal_probability_outside(lo: float, hi: float, mu: float = 0, sigma: float = 1):
    return 1 - normal_probability_between(lo, hi, mu, sigma)


from lesson5 import inverse_normal_cdf


def normal_upper_bound(probability: float,
                       mu: float = 0,
                       sigma: float = 1) -> float:
    return inverse_normal_cdf(probability, mu, sigma)


def normal_lower_bound(probability: float,
                       mu: float = 0,
                       sigma: float = 1) -> float:
    return inverse_normal_cdf(1- probability, mu, sigma)


def normal_two_sided_bounds(probability: float, mu: float = 0, sigma: float = 1) -> Tuple[float, float]:
    tail_probability = (1 - probability) / 2
    upper_bound = normal_lower_bound(tail_probability, mu, sigma)
    lower_bound = normal_upper_bound(tail_probability, mu, sigma)
    return lower_bound, upper_bound


mu_0, sigma_0 = normal_approximation_to_binomial(1000, 0.5)


lower_bound, upper_bound = normal_two_sided_bounds(0.95, mu_0, sigma_0)


lo, hi = normal_two_sided_bounds(0.95, mu_0, sigma_0)
mu_1, sigma_1 = normal_approximation_to_binomial(1000, 0.55)
type2_probability = normal_probability_between(lo, hi, mu_1, sigma_1)
power = 1 - type2_probability
hi = normal_upper_bound(0.95, mu_0, sigma_0)
type2_probability = normal_probability_below(hi, mu_1, sigma_1)
power = 1 - type2_probability


def two_sided_p_value(x: float, mu: float =0, sigma: float = 1) -> float:
    if x >= mu:
        return 2 * normal_probability_above(x, mu, sigma)
    else:
        return 2 * normal_probability_below(x, mu, sigma)


two_sided_p_value(529.5, mu_0, sigma_0)

import random

extreme_value_count = 0
for _ in range(1000):
    num_heads = sum(1 if random.random() < 0.5 else 0
                    for _ in range(1000))
    if num_heads >= 530 or num_heads <= 470:
        extreme_value_count += 1


assert 59 < extreme_value_count < 65, f'{extreme_value_count}'
two_sided_p_value(531.5, mu_0, sigma_0)

upper_p_value = normal_probability_above
lower_p_value = normal_probability_below
upper_p_value(524.5, mu_0, sigma_0)
upper_p_value(526.5, mu_0, sigma_0)


# p-hacking

from typing import List


def run_experiment() -> List[bool]:
    return [random.random() < 0.5 for _ in range(1000)]


def reject_fairness(experiment: List[bool]) -> bool:
    num_heads = len([flip for flip in experiment if flip])
    return num_heads < 469 or num_heads > 531


random.seed(0)
experiments = [run_experiment() for _ in range(1000)]
num_rejections = len([experiment
                      for experiment in experiments
                      if reject_fairness(experiment)])

assert num_rejections == 46


def estimated_parameters(N: int, n: int):
    p = n / N
    sigma = math.sqrt(p * (1 - p) / N)
    return p, sigma
