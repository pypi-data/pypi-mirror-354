from typing import Callable
import itertools

import numpy as np
from tqdm import tqdm

from ..helper.exact import compute_weights


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

    # Calculate factorials for efficiency
    factorials_vec = np.vectorize(np.math.factorial, otypes=["int64"])
    factorials = factorials_vec(np.arange(n + 1))
    weights = compute_weights(factorials, n)
    weights = np.append([1], weights)

    # harmonic_sums = [sum(1 / i for i in range(subset_size, n + 1)) for subset_size in range(1, n+1)]
    indices = np.arange(1, n + 1)
    cumulative_harmonics = np.cumsum(1 / indices[::-1])[::-1]
    harmonic_sums = np.append([0], cumulative_harmonics)

    utility_cache = {}

    for player_i in tqdm(players):
        # NOTE: FOLLOWING LINE ONLY USABLE IN CONJUNCTION WITH COMMENTED OUT CODE AT THE END
        # ONLY USABLE IF WE CAN ASSUME SYMMETRIC MATRIX
        # for player_j in range(player_i, n):
        for player_j in players:
            sum_ij = 0
            for subset in itertools.chain.from_iterable(itertools.combinations(players, r) for r in range(n + 1)):
                subset_size = len(subset)

                # weight = (factorials[subset_size - 1] * factorials[n - subset_size]) / factorials[n]
                subset_without_player_i = tuple(get_set_without_players(set(subset), [player_i]))
                subset_without_player_j = tuple(get_set_without_players(set(subset), [player_j]))
                subset_without_player_i_and_without_player_j = tuple(get_set_without_players(set(subset), [player_i, player_j]))

                if subset not in utility_cache:
                    utility_cache[subset] = utility_game_function(set(subset))
                if subset_without_player_i not in utility_cache:
                    utility_cache[subset_without_player_i] = utility_game_function(set(subset_without_player_i))
                if subset_without_player_j not in utility_cache:
                    utility_cache[subset_without_player_j] = utility_game_function(set(subset_without_player_j))
                if subset_without_player_i_and_without_player_j not in utility_cache:
                    utility_cache[subset_without_player_i_and_without_player_j] = utility_game_function(set(subset_without_player_i_and_without_player_j))

                adapted_marginal_contribution = utility_cache[subset] - utility_cache[subset_without_player_i] - utility_cache[subset_without_player_j] + utility_cache[subset_without_player_i_and_without_player_j]
                # adapted_marginal_contribution = utility_game_function(subset) \
                #                                 - utility_game_function(subset_without_player_i) \
                #                                 - utility_game_function(subset_without_player_j) \
                #                                 + utility_game_function(subset_without_player_i_and_without_player_j)

                #sum_ij += weights[subset_size] * adapted_marginal_contribution * harmonic_sums[subset_size]
                # The following line is a try to compute the same for banzhaf instead of only for shapley, but i am not sure if it works, because we dont have eficiency which is used in a proof
                # i have to check the proof in the appendix to check if it is needed there, or only such that it adds up to the real banzhaf value
                # values dont add up to banzhaf values, but they are not gibberish, so may still be useful
                # could be worth investigating experimentally
                sum_ij += (1/(2 ** (n - 1))) * adapted_marginal_contribution * harmonic_sums[subset_size]
            # shapley_values[player_i, player_j] = round(sum_ij, 3)
            shapley_values[player_i, player_j] = sum_ij

    # FOLLOWING: ONLY USABLE IF WE KNOW THAT THE MATRIX IS SYMMETRIC in CONJUNCTION WITH LOOP ITERATION CHANGE
    # Mirror the upper triangular part to the lower triangular part
    # i_upper = np.triu_indices(n, k=1)  # Get the indices of the upper triangular part excluding diagonal
    # shapley_values[(i_upper[1], i_upper[0])] = shapley_values[i_upper]  # Mirror to the lower triangular part

    return shapley_values


def get_set_without_players(S, players: list):
    subset_without_players = S.copy()
    for player in players:
        subset_without_players.discard(player)
    return subset_without_players
