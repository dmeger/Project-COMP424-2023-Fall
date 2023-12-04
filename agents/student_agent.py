# Student agent: Add your own agent here
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
        # Translate the observation into your game state representation

        # Call the alpha-beta search to get the best move
        best_move = self.alpha_beta_search(obs)
        return best_move

        # dummy return
        # return my_pos, self.dir_map["u"]
 
    def alpha_beta_search(self, state):
        # Implement the alpha-beta search algorithm
        # Initialize alpha and beta values
        alpha = float('-inf')
        beta = float('inf')

        # Initially call the max_value function
        best_score, best_move = self.max_value(state, alpha, beta, 0)
        return best_move

    def max_value(self, state, alpha, beta, depth):
        # Check for terminal state or maximum depth
        if self.is_terminal(state) or depth == MAX_DEPTH:
            return self.evaluate(state), None

        v = float('-inf')
        best_move = None
        for move in self.get_possible_moves(state):
            # Apply the move
            new_state = self.apply_move(state, move)
            # Call min_value
            min_v, _ = self.min_value(new_state, alpha, beta, depth + 1)
            if min_v > v:
                v = min_v
                best_move = move
            if v >= beta:
                return v, best_move
            alpha = max(alpha, v)
        return v, best_move

    def min_value(self, state, alpha, beta, depth):
        # Check for terminal state or maximum depth
        if self.is_terminal(state) or depth == MAX_DEPTH:
            return self.evaluate(state), None

        v = float('inf')
        best_move = None
        for move in self.get_possible_moves(state):
            # Apply the move
            new_state = self.apply_move(state, move)
            # Call max_value
            max_v, _ = self.max_value(new_state, alpha, beta, depth + 1)
            if max_v < v:
                v = max_v
                best_move = move
            if v <= alpha:
                return v, best_move
            beta = min(beta, v)
        return v, best_move
    
    def evaluate(self, state):
        # Evaluate the game state and return a heuristic score
        # ...
        return 0

    def is_terminal(self, state):
        # Determine if the game state is a terminal state
        # ...
        return False

    def get_possible_moves(self, state):
        # Generate and return all possible legal moves from the current state
        # ...
        return 0

    def apply_move(self, state, move):
        # Apply a move to the state and return the new state
        # ...
        return 0

    def parse_observation(self, obs):
        # Translate the observation into a game state representation
        # ...
        return 0
