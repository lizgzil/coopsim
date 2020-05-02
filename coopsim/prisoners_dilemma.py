import numpy as np
from numpy import random

import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.animation as animation

class PrisonersDilemma:

    """
    Input: 
        payoffs: A dictionary containing each pair combination payoff
            t : one player C one player D, D gets t
            r : both players C, they both get r
            p : both defect, both get p
            s : one player C one player D, C gets s
            t>r>p>s
        grid_len: (int) Number of pixels in game grid
        init_coop: (0-1) Initial proportion of cooperators
        num_iterations: (int) Number of iterations of the game
        special_init: (bool) If true then start with one defector in the middle (default to True)
        rand_seed: (int) Which random seed to use (default to None)


    Strategies:
        0 : Defector
        1 : Cooperator
        

    """

    def __init__(
        self, payoffs, grid_len, init_coop, num_iterations,
        special_init=True, rand_seed=None
        ):

        self.payoffs = payoffs
        # self.payoff_t = payoffs['t']
        # self.payoff_r = payoffs['r']
        # self.payoff_p = payoffs['p']
        # self.payoff_s = payoffs['s']

        self.grid_len = grid_len
        self.init_coop = init_coop
        self.num_iterations = num_iterations
        self.special_init = special_init
        self.rand_seed = rand_seed

        self.init_strategies, grid_nan = self.initialise_game()

        self.init_fitnesses = grid_nan
        self.init_changes = grid_nan
        

    def initialise_game(self):

        if self.special_init == False:
            # Randomly 1 (C) or 0 (D)
            if self.rand_seed:
                random.seed(self.rand_seed)
            strategies = np.random.choice(
                [0, 1],
                size = (self.grid_len, self.grid_len),
                p = [1 - self.init_coop, self.init_coop]
                )
        else:
            # One defector in the middle of defectors
            strategies = np.ones((self.grid_len, self.grid_len), dtype = np.int8)
            strategies[round(self.grid_len/2), round(self.grid_len/2)] = 0

        grid_nan = np.empty((self.grid_len, self.grid_len,))
        grid_nan[:] = np.nan

        return strategies, grid_nan

    def play_game(self, player_1_strategy, player_2_strategy):

        '''
        1 (C) or 0 (D)
        both defect, both get p
        one player C one player D, D gets t
        one player C one player D, C gets s
        both players C, they both get r   
        '''

        if ((player_1_strategy == 0) & (player_2_strategy == 0)):
            player_1_payoff = self.payoffs['p']
            player_2_payoff = self.payoffs['p']
        elif ((player_1_strategy == 0) & (player_2_strategy == 1)):
            player_1_payoff = self.payoffs['t']
            player_2_payoff = self.payoffs['s']
        elif ((player_1_strategy == 1) & (player_2_strategy == 0)):
            player_1_payoff = self.payoffs['s']
            player_2_payoff = self.payoffs['t']
        elif ((player_1_strategy == 1) & (player_2_strategy == 1)):
            player_1_payoff = self.payoffs['r']
            player_2_payoff = self.payoffs['r']
        else:
            print("Error - player strategies are not 1 or 0")

        return player_1_payoff, player_2_payoff


    def get_neighbour_qualities(self, player_qualities):
    
        down_neighbour = np.roll(player_qualities, -1, axis=0) # down
        up_neighbour = np.roll(player_qualities, 1, axis=0) # up
        left_neighbour = np.roll(player_qualities, -1, axis=1) # left
        right_neighbour = np.roll(player_qualities, 1, axis=1) # right
        
        nw_neighbour = np.roll(up_neighbour, -1, axis=1) # north west
        ne_neighbour = np.roll(up_neighbour, 1, axis=1) # north east
        sw_neighbour = np.roll(down_neighbour, -1, axis=1) # south west
        se_neighbour = np.roll(down_neighbour, 1, axis=1) # south east
        
        return (down_neighbour, up_neighbour, left_neighbour, right_neighbour,
                nw_neighbour, ne_neighbour, sw_neighbour, se_neighbour)

    def get_cell_payoff(self, strategies,
                    down_neighbour,
                    up_neighbour,
                    left_neighbour,
                    right_neighbour,
                    nw_neighbour,
                    ne_neighbour,
                    sw_neighbour,
                    se_neighbour,
                    row, col):
        '''
        Where they all play the game with each other to get their total payoffs
        '''
        payoff_down_cell, _ = self.play_game(strategies[row,col], down_neighbour[row,col])
        payoff_up_cell, _ = self.play_game(strategies[row,col], up_neighbour[row,col])
        payoff_left_cell, _ = self.play_game(strategies[row,col], left_neighbour[row,col])
        payoff_right_cell, _ = self.play_game(strategies[row,col], right_neighbour[row,col])
        
        payoff_nw_cell, _ = self.play_game(strategies[row,col], nw_neighbour[row,col])
        payoff_ne_cell, _ = self.play_game(strategies[row,col], ne_neighbour[row,col])
        payoff_sw_cell, _ = self.play_game(strategies[row,col], sw_neighbour[row,col])
        payoff_se_cell, _ = self.play_game(strategies[row,col], se_neighbour[row,col])
        
        payoff_itself, _ = self.play_game(strategies[row,col], strategies[row,col])

        payoff = (payoff_down_cell + payoff_up_cell + payoff_left_cell + payoff_right_cell +
                 payoff_nw_cell + payoff_ne_cell + payoff_sw_cell + payoff_se_cell + payoff_itself)
        

        return payoff

    def get_strategy_change_code(self, old_strat, new_strat):
        '''
        0 = stayed as D 
        1 = stayed as C 
        2 = changed from D to C
        3 = changed from C to D
        '''
        if ((old_strat == 0) & (new_strat == 0)):
            change_code = 0
        elif ((old_strat == 0) & (new_strat == 1)):
            change_code = 2
        elif ((old_strat == 1) & (new_strat == 0)):
            change_code = 3 
        else:
            change_code = 1
        return change_code

    def run_iteration(self, strategies, fitnesses, changes):

        # Get the neighbour's strategies:

        (down_neighbour,
         up_neighbour,
         left_neighbour,
         right_neighbour,
         nw_neighbour,
         ne_neighbour,
         sw_neighbour,
         se_neighbour) = self.get_neighbour_qualities(strategies)

        # Get every cell's payoff (makes no difference if row and col for loops are other way):
        for row in range(0, self.grid_len):
            for col in range(0, self.grid_len):
                fitnesses[row, col] = self.get_cell_payoff(strategies,
                                                        down_neighbour,
                                                        up_neighbour,
                                                        left_neighbour,
                                                        right_neighbour,
                                                        nw_neighbour,
                                                        ne_neighbour,
                                                        sw_neighbour,
                                                        se_neighbour,
                                                        row, col)

        # Get the neighbour's payoffs:
        (down_neighbour_payoff,
         up_neighbour_payoff,
         left_neighbour_payoff,
         right_neighbour_payoff,
         nw_neighbour_payoff,
         ne_neighbour_payoff,
         sw_neighbour_payoff,
         se_neighbour_payoff) = self.get_neighbour_qualities(fitnesses)


        # Consider your neighbours and change if they do better
        for row in range(0, self.grid_len):
            for col in range(0, self.grid_len):
                # Get previous strategy
                old_strat = strategies[row, col]
                # Neighbours strategies
                neigh_strats = [
                    right_neighbour[row, col],
                    left_neighbour[row, col],
                    up_neighbour_payoff[row, col],
                    down_neighbour_payoff[row, col],
                    nw_neighbour[row, col],
                    ne_neighbour[row, col],
                    sw_neighbour[row, col],
                    se_neighbour[row, col]]
                # If all the neighbours have the same strategy as you, don't do anything
                if ((old_strat==neigh_strats[0]) and (len(set(neigh_strats))==1)):
                    strategies[row, col] = old_strat
                else:
                    # All the surrounding payoffs and your own
                    b = np.array([right_neighbour_payoff[row,col], left_neighbour_payoff[row,col],
                                  up_neighbour_payoff[row,col], down_neighbour_payoff[row,col],
                                  nw_neighbour_payoff[row,col],
                                  ne_neighbour_payoff[row,col],
                                  sw_neighbour_payoff[row,col],
                                  se_neighbour_payoff[row,col]])

                    if fitnesses[row, col] >= b.max():
                        strategies[row, col] = old_strat
                    else:
                        # TO DO: if there is a higher fitness
                        # then it'll be from the other strategy.
                        # since there cant be a tie when the strat is the same
                        # So you can just pick the opposite rather than this index stuff

                        # Get the index of the highest
                        best_index = np.random.choice(np.flatnonzero(b == b.max())) # if the same pick one randomly
                        
                        # Update to the strategy of this 'best' cell
                        strategies[row, col] = [right_neighbour[row,col], left_neighbour[row,col],
                                                up_neighbour[row,col], down_neighbour[row,col],
                                                nw_neighbour[row,col], ne_neighbour[row,col],
                                                sw_neighbour[row,col], se_neighbour[row,col]][best_index]

                # Get colour matrix
                changes[row, col] = self.get_strategy_change_code(old_strat, strategies[row, col])

        return strategies, changes

    def run_simulation(self):

        strategies = self.init_strategies
        changes = self.init_changes
        fitnesses = self.init_fitnesses

        strategies_all = []
        changes_all =[]

        for i in range(0, self.num_iterations):
            if i%10==0:
                print("Running iteration " + str(i))

            strategies, changes = self.run_iteration(strategies, fitnesses, changes)
            strategies_all.append(strategies.copy())
            changes_all.append(changes.copy())

            if len(set(np.array(strategies_all).flatten()))==1:
                print("All strategies the same, stopping")
                return strategies_all, changes_all

        return strategies_all, changes_all

