# Student agent: Add your own agent here
from agents.agent import Agent
from store import register_agent
import sys
import numpy as np
from copy import deepcopy
import time


@register_agent("student_agent")
class StudentAgent(Agent):

    def __init__(self):
        super(StudentAgent, self).__init__()
        self.name = "StudentAgent"
        self.autoplay = True
        self.dir_map = {
            "u": 0,
            "r": 1,
            "d": 2,
            "l": 3,
        }

    def step(self, chess_board, my_pos, adv_pos, max_step):
        max_depth = 5
        start_time = time.time()

        alpha = float('-inf')
        beta = float('-inf')
        v = float('-inf')
        best_moves = []

        for move in self.allowed_moves(chess_board, my_pos, max_step, adv_pos):
            # Apply the move
            chess_board = self.apply_move(chess_board, move)
            
            # call min_value
            if max_depth == 0 or self.is_terminal(chess_board, move):
                value = self.evaluate(chess_board, move, adv_pos, max_step)
            else:
                value = self.min_value(chess_board, move, adv_pos, max_step, alpha, beta, max_depth - 1, start_time)
            if value > v:
                v = value
                best_moves.clear()
                best_moves.append(move)
            if v >= value:
                break
            alpha = max(alpha, v)
            
            # Make sure each move takes less than 2 seconds
            time_taken = time.time() - start_time
            if time_taken > 1.85:
                break

        i = 0
        if len(best_moves) > 1:
            length_list = len(best_moves)
            i = np.random.randint(0, length_list)

        r, c, d = best_moves[i]
        return (r, c), d

    def max_value(self, chess_board, move, adv_pos, max_step, alpha, beta, max_depth, start_time): 
        v = float('-inf')
        # Make sure each move takes less than 2 seconds
        if max_depth == 0 or self.is_terminal(chess_board, move):
            return self.evaluate(chess_board, move, adv_pos, max_step)
        
        m_r, m_c, m_d = move
        for moves in self.allowed_moves(chess_board, (m_r, m_c), max_step, adv_pos):
            chess_board = self.apply_move(chess_board, moves)
            # score = self.evaluate(chess_board, moves, adv_pos, max_step)
            min_v = self.min_value(chess_board, moves, adv_pos, max_step, alpha, beta, max_depth - 1, start_time)
            if min_v > v:
                v = min_v
            if v >= beta: 
                return v
            alpha = max(alpha, v)
            # time check
            time_taken = time.time() - start_time
            if time_taken > 1.85:
                break
        return v

    def min_value(self, chess_board, move, adv_pos, max_step, alpha, beta, max_depth, start_time):
        v = float('inf')
        if max_depth == 0 or self.is_terminal(chess_board, move):
            return self.evaluate(chess_board, move, adv_pos, max_step)
        
        m_r, m_c, m_d = move
        for moves in self.allowed_moves(chess_board, adv_pos, max_step, (m_r, m_c)):
            chess_board = self.apply_move(chess_board, moves)
            # score = self.evaluate(chess_board, move, adv_pos, max_step)
            max_v = self.max_value(chess_board, moves, adv_pos, max_step, alpha, beta, max_depth - 1, start_time)
            if max_v < v:
                v = max_v
            if v <= alpha:
                return v
            beta = min(beta, v)
            # time check
            time_taken = time.time() - start_time
            if time_taken > 1.85:
                break
        return v

    def check_boundary(self, chess_board, dest_pos):
        r, c = dest_pos
        # Wall coordinates
        wall = int(chess_board[0].size/4) - 1
        return 0 <= r < wall and 0 <= c < wall

    def check_valid_step(self, chess_board, start_pos, end_pos, d, max_step, adv_pos):
        # CODE TAKEN FROM WORLD.py

        chess_board = deepcopy(chess_board)
        moves = ((-1, 0), (0, 1), (1, 0), (0, -1))
        # Endpoint already has barrier or is border
        r, c = end_pos

        if not self.check_boundary(chess_board, end_pos):
            return False
        if chess_board[r, c, d]:
            return False
        if np.array_equal(start_pos, end_pos):
            return True

        # BFS
        state_queue = [(start_pos, 0)]
        visited = {tuple(start_pos)}
        is_reached = False
        while state_queue and not is_reached:
            cur_pos, cur_step = state_queue.pop(0)
            r, c = cur_pos
            if cur_step == max_step:
                break
            for dir, move in enumerate(moves):
                if chess_board[r, c, dir]:
                    continue

                r1, c1 = move
                r2, c2 = cur_pos

                next_pos = (r2 + r1, c2 + c1)

                if np.array_equal(next_pos, adv_pos) or tuple(next_pos) in visited:
                    continue
                if np.array_equal(next_pos, end_pos):
                    is_reached = True
                    break

                visited.add(tuple(next_pos))
                state_queue.append((next_pos, cur_step + 1))

        return is_reached

    def allowed_moves(self, chess_board, my_pos, max_step, adv_pos):

        move_list = []      # Initialize a list of moves
        r, c = my_pos       # separate my_pos into x and y coordinates
        r_1 = r - max_step   
        c_1 = c              

        # for each direction move and wall for max_step
        for d in range(4):
            for x in range(max_step + 1):
                for y in range(-x, x + 1, 1):
                    if self.check_valid_step(chess_board, my_pos, (r_1 + x, c_1 + y), d, max_step, adv_pos):
                        move_list.append((r_1 + x, c_1 + y, d))

            r_2 = r + max_step
            c_2 = c
            for x in range(max_step - 1, -1, -1):
                for y in range(-x, x + 1, 1):
                    if self.check_valid_step(chess_board, my_pos, (r_2 - x, c_2 - y), d, max_step, adv_pos):
                        move_list.append((r_2 - x, c_2 - y, d))

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