from typing import Callable
import itertools

import numpy as np
from tqdm import tqdm

from scipy.special import factorial

def compute_weights(factorials, n):
    return factorials[:-1] * factorials[n - 1::-1] / factorials[n]

def shapley_value(utility_game_function: Callable, n: int):
    """
    Parameters:
    utility_game_function (Callable): Function which represents the game.
    n (int): number of players

    Returns:
    List[Float]: The computed shapley values
    """
    players = np.arange(n)
    shapley_values = np.zeros((n, n))

    # Calculate factorials beforehand for efficiency
    factorials = factorial(np.arange(n + 1), exact=True)
    weights = compute_weights(factorials, n)
    utility_cache = {}

    print(f"Progress bar: Computing Shapley Value for {n} players:")
    for player in tqdm(players):
        for subset in itertools.chain.from_iterable(itertools.combinations(players, r) for r in range(n + 1)):
            if player not in subset:
                subset_with_player = subset + (player,)

                if subset not in utility_cache:
                    utility_cache[subset] = utility_game_function(set(subset))
                if subset_with_player not in utility_cache:
                    utility_cache[subset_with_player] = utility_game_function(set(subset_with_player))
                marginal_contribution = utility_cache[subset_with_player] - utility_cache[subset]

                shapley_values[player, len(subset)] += marginal_contribution

        for i in range(len(players)):
            shapley_values[player, i] = shapley_values[player, i] * weights[i]
    return shapley_values
