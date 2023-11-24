# Student agent: Add your own agent here
from math import inf
from agents.agent import Agent
from store import register_agent
import sys
import numpy as np
from copy import deepcopy
import time


@register_agent("student_agent")
class StudentAgent(Agent):
    """
    A dummy class for your implementation. Feel free to use this class to
    add any helper functionalities needed for your agent.
    """

    def __init__(self):
        super(StudentAgent, self).__init__()
        self.name = "StudentAgent"
        self.dir_map = {
            "u": 0,
            "r": 1,
            "d": 2,
            "l": 3,
        }

    def step(self, chess_board, my_pos, adv_pos, max_step):
        """
        Implement the step function of your agent here.
        You can use the following variables to access the chess board:
        - chess_board: a numpy array of shape (x_max, y_max, 4)
        - my_pos: a tuple of (x, y)
        - adv_pos: a tuple of (x, y)
        - max_step: an integer

        You should return a tuple of ((x, y), dir),
        where (x, y) is the next position of your agent and dir is the direction of the wall
        you want to put on.

        Please check the sample implementation in agents/random_agent.py or agents/human_agent.py for more details.
        """

        # Some simple code to help you with timing. Consider checking 
        # time_taken during your search and breaking with the best answer
        # so far when it nears 2 seconds.
        start_time = time.time()
        time_taken = time.time() - start_time
        
        print("My AI's turn took ", time_taken, "seconds.")

        # dummy return
        return my_pos, self.dir_map["u"]

    def is_valid_move(self, new_pos, my_pos, adv_pos, chess_board):
        """
        Checks if the agent can move to the proposed position based on the following criteria:
        - Position is not outside the chess_board
        - Position is not diagonal to the current
        - Position does not contain the adversary
        - There's no wall between the current and new position

        :pre: Assumes that the player hasn't surpassed k moves
        :return: True if position is valid, False otherwise
        """
        #TODO: Implement

        pass

    def is_valid_wall_placement(self, new_wall_pos, my_pos, chess_board):
        """
        Checks if a barrier can be placed at the proposed spot
        - Can't be placed on a spot where there's an existing barrier
        - Can't be placed on the boundaries of the chess board
        
        :pre: assumes that the player has already moved (my_pos = new_pos)
        :return: True if barrier can be placed, False otherwise
        """
        #TODO: Rippppppp this mf
        pass

    def minimax_decision(self, state):
        """
        Determines the best action by applying the minimax algorithm.
        :param state: The current state of the game.
        :return: The best action for the current player.
        """
        pass

    def max_value(self, state, alpha, beta):
        """
        Computes the maximum utility value for the maximizing player.
        :param state: The current state of the game.
        :param alpha: The value of the best alternative for the max player along the path to state.
        :param beta: The value of the best alternative for the min player along the path to state.
        :return: The utility value of the state for the maximizing player.
        """
        pass

    def min_value(self, state, alpha, beta):
        """
        Computes the minimum utility value for the minimizing player.
        :param state: The current state of the game.
        :param alpha: The value of the best alternative for the max player along the path to state.
        :param beta: The value of the best alternative for the min player along the path to state.
        :return: The utility value of the state for the minimizing player.
        """
        pass

    def terminal_test(self, state):
        """
        Tests if the game has reached a terminal state.
        :param state: The current state of the game.
        :return: Boolean indicating whether the state is terminal.
        """
        pass

    def utility(self, state, player):
        """
        Calculates the utility of a terminal state for a given player.
        :param state: The current state of the game.
        :param player: The player for whom to calculate the utility.
        :return: The utility value for the player.
        """
        pass

    def actions(self, state):
        """
        Returns the set of possible actions available in the current state.
        :param state: The current state of the game.
        :return: A list of all possible actions.
        """
        pass

    def result(self, state, action):
        """
        Returns the state that results from performing a given action on the current state.
        :param state: The current state of the game.
        :param action: The action to be performed.
        :return: The resulting state after the action is taken.
        """
        pass
