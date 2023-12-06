# Student agent: Add your own agent here
from agents.agent import Agent
from store import register_agent
import sys
import numpy as np
from copy import deepcopy
import time

moves = ((-1, 0), (0, 1), (1, 0), (0, -1))

@register_agent("student_agent")
class StudentAgent(Agent):

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

        #start_time = time.time()
        #time_taken = time.time() - start_time
        #print("My AI's turn took ", time_taken, "seconds.")

        # include directions
        m_r, m_c = my_pos
        my_pos = (m_r, m_c, 0)

        v = float('-inf')
        list_best_moves = []

        for moves in self.allowed_moves(chess_board, (m_r, m_c), max_step, adv_pos):
            # Apply the move
            chess_board = self.apply_move(chess_board, moves)
            
            if self.is_terminal(chess_board, moves):
                value = self.evaluate(chess_board, moves, adv_pos, max_step)
            else:
                # call min_value
                value = self.min_value(chess_board, moves, adv_pos, max_step)
            if value > v:
                v = value
                list_best_moves.clear()
                list_best_moves.append(moves)

            if value == v:
                list_best_moves.append(moves)

        a = 0
        if len(list_best_moves) > 1:
            length_list = len(list_best_moves)
            a = np.random.randint(0, length_list)

        r, c, d = list_best_moves[a]
        return (r, c), d
    
    def max_value(self, chess_board, original_position, adv_pos, max_step): 
        v = float('-inf')
        m_r, m_c, m_d = original_position
        for moves in self.allowed_moves(chess_board, (m_r, m_c), max_step, adv_pos):
            chess_board = self.apply_move(chess_board, moves)
            score = self.evaluate(chess_board, moves, adv_pos, max_step)
            if score > v:
                v = score
        return v

    def min_value(self, chess_board, original_position, adv_pos, max_step):
        v = float('inf')
        m_r, m_c, m_d = original_position
        for moves in self.allowed_moves(chess_board, adv_pos, max_step, (m_r, m_c)):
            chess_board = self.apply_move(chess_board, moves)
            score = self.evaluate(chess_board, original_position, adv_pos, max_step)
            if score < v:
                v = score

        return v

    def check_boundary(self, chess_board, pos):
        r, c = pos
        si = int(chess_board[0].size/4)
        si = si - 1
        return 0 <= r < si and 0 <= c < si

    def check_valid_step(self, chess_board, start_pos, end_pos, barrier_dir, max_step1, adv_pos):
        # Endpoint already has barrier or is boarder
        chess_board = deepcopy(chess_board)

        r, c = end_pos

        if not self.check_boundary(chess_board, end_pos):
            return False

        if chess_board[r, c, barrier_dir]:
            return False
        
        return True

    def allowed_moves(self, chess_board, my_pos, max_step, adv_pos):

        move_list = []      # Initialize a list of moves
        r, c = my_pos       # separate my_pos into x and y coordinates
        r1 = r - max_step   
        c1 = c              

        # for each direction move and wall for max_step
        for d in range(4):
            for x in range(max_step + 1):
                for y in range(-x, x + 1, 1):
                    if self.check_valid_step(chess_board, my_pos, (r1 + x, c1 + y), d, max_step, adv_pos):
                        move_list.append((r1 + x, c1 + y, d))

            r2 = r + max_step
            c2 = c
            for x in range(max_step - 1, -1, -1):
                for y in range(-x, x + 1, 1):
                    if self.check_valid_step(chess_board, my_pos, (r2-x,c2-y), d, max_step, adv_pos):
                        move_list.append((r2 - x, c2 - y, d))

        return move_list

    def is_terminal(self, chess_board, my_pos):
        #code taken from random_agent.py
        
        r, c, d = my_pos
        allowed_barriers=[i for i in range(0,4) if not chess_board[r,c,i]]
        return not(len(allowed_barriers)>=1) 
    
    def evaluate(self, chess_board, my_pos, adv_pos, max_step):
        # Evaluate the game state and return a heuristic score
        m_r, m_c, m_d = my_pos
        
        score1 = len(self.allowed_moves(chess_board, (m_r, m_c), max_step, adv_pos))
        score2 = len(self.allowed_moves(chess_board, adv_pos, max_step, (m_r, m_c)))
        score = score1 - score2
        
        return score
    
    def apply_move(self, chess_board, move):
        # Apply a move to the state and return the new state
        chess_board = deepcopy(chess_board)
        r, c, d = move

        chess_board[r, c, d] = True
        return chess_board