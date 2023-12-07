# Student agent: Add your own agent here
from agents.agent import Agent
from store import register_agent
import sys
import numpy as np
from copy import deepcopy
import time
import random

#possible move steps: up, right, down, left
moves = ((-1, 0), (0, 1), (1, 0), (0, -1))

@register_agent("student_agent")
class StudentAgent(Agent):
    """
    A dummy class for your implementation. Feel free to use this class to
    add any helper functionalities needed for your agent.
    """
    def __init__(self):
        super(StudentAgent, self).__init__()
        self.name = "StudentAgent"
        self.MOVE_NUMBER = 0
        self.dir_map = {
            "u": 0,
            "r": 1,
            "d": 2,
            "l": 3,
        }


    #helper functions
    def all_valid_moves(self, chess_board, my_pos, max_step, adv_pos):
        valid_moves = []

        # BFS
        state_queue = [(my_pos, 0)]
        visited = {my_pos}

        while state_queue:
            cur_pos, cur_step = state_queue.pop(0)

            if cur_step == max_step:
                break

            for dir, move in enumerate(moves):
                # if barrier between current pos and move, continue
                if chess_board[cur_pos[0], cur_pos[1], dir]:
                    continue
                
                # set new position
                next_pos = tuple(np.array(cur_pos) + np.array(move))
                #if cell is already visited, continue
                if next_pos in visited:
                    continue

                # if position is adversary position, continue
                if np.array_equal(next_pos, adv_pos):
                    continue

                # now that we can go to next_pos, check all four possible barrier placements
                visited.add(next_pos)
                state_queue.append((next_pos, cur_step + 1))

        #now add possible valid moves in next_pos when there is no barrier
        for pos in visited:
            for i in range(4):
                if chess_board[pos[0], pos[1], i]:
                    continue
                valid_moves.append((pos, i))

        return valid_moves

    

    def move_in(self, chess_board, move):
        """
        Return the new chess board after making the move
        :param chess_board: the current chess board
        :param move: the move to be made

        :return: the new chess board
        """

        new_board = deepcopy(chess_board)
        (x, y), dir = move
        new_board[x, y, dir] = 1
        return new_board
    
    def valid_moves_adv_after_move(self, chess_board, move, max_step, adv_pos):
        """
        Return all valid moves for the adversary agent after the move is made
        :param chess_board: the current chess board
        :param my_pos: the position of my agent
        :param max_step: the maximum number of steps
        :param adv_pos: the position of the adversary agent
        :param move: the move to be made

        :return: a list of valid moves
        """

        new_board = self.move_in(chess_board, move)
        my_pos = move[0]
        return self.all_valid_moves(new_board, adv_pos, max_step, my_pos)


    #modified function given in world.py
    def check_endgame(self, chess_board, original_position, opponent_pos):
        """
        Check if the game ends and compute the current score of the agents.

        Returns
        -------
        is_endgame : bool
            Whether the game ends.
        player_1_score : int
            The score of player 1.
        player_2_score : int
            The score of player 2.
        """
        # Union-Find
        father = dict()
        for r in range(chess_board.shape[0]):
            for c in range(chess_board.shape[1]):
                father[(r, c)] = (r, c)

        def find(pos):
            if father[pos] != pos:
                father[pos] = find(father[pos])
            return father[pos]

        def union(pos1, pos2):
            father[pos1] = pos2

        for r in range(chess_board.shape[0]):
            for c in range(chess_board.shape[1]):
                for dir, move in enumerate(
                    moves[1:3]
                ):  # Only check down and right
                    if chess_board[r, c, dir + 1]:
                        continue
                    pos_a = find((r, c))
                    pos_b = find((r + move[0], c + move[1]))
                    if pos_a != pos_b:
                        union(pos_a, pos_b)

        for r in range(chess_board.shape[0]):
            for c in range(chess_board.shape[1]):
                find((r, c))
        p0_r = find(tuple(original_position))
        p1_r = find(tuple(opponent_pos))
        p0_score = list(father.values()).count(p0_r)
        p1_score = list(father.values()).count(p1_r)
        if p0_r == p1_r:
            player_win = None
            return False, 1/2
        win_blocks = -1
        if p0_score > p1_score:
            # Player 0 wins (our agent)
            player_win = 0
            win_blocks = p0_score
        elif p0_score < p1_score:
            # Player 1 wins (adversary agent)
            player_win = 1
            win_blocks = p1_score
        else:
            # Player 0 and Player 1 tie
            player_win = -1  # Tie
            return True, 1/2
        if player_win >= 0:
            diff_score = (p0_score - p1_score)/win_blocks
            return True, diff_score


    #defining four heuristic functions
    def chasing_adversary_heuristic(self, chess_board, move, adv_pos, max_step):
        """
        Heuristic function for chasing the adversary by computing the Manhattan distance between the given move and the adversary agent and normalizing it by the maximum possible distance between two agents in the board
        :param chess_board: the current chess board
        :param my_pos: the position of my agent
        :param adv_pos: the position of the adversary agent
        :param max_step: the maximum number of steps

        :return: the heuristic value
        """

        (x, y), dir = move

        max_dist_between_agents = 2 * (chess_board.shape[0] -1)

        return abs(x - adv_pos[0]) + abs(y - adv_pos[1]) / max_dist_between_agents

    
    def center_heuristic(self, chess_board, move, adv_pos, max_step):
        """

        Heuristic function for computing the Manhttan distance between my agent and the center of the board and normalizing it by the maximum possible distance between my agent and the center of the board

        :param chess_board: the current chess board
        :param my_pos: the position of my agent
        :param adv_pos: the position of the adversary agent
        :param max_step: the maximum number of steps

        :return: the heuristic value
        """

        (x, y), dir = move

        max_dist_center = chess_board.shape[0]

        return abs(x - chess_board.shape[0] // 2) + abs(y - chess_board.shape[1] // 2) / max_dist_center
    
    def blocking_adversary_heuristic(self, chess_board, move, adv_pos, max_step):
        """
        
        Heuristic function for blocking the adversary by minimizing the number of valid moves of the adversary agent that is initially 1+2K(K+1) normalzing it by the maximum possible number of valid moves of the adversary agent (1+2K(K+1))
        :param chess_board: the current chess board
        :param my_pos: the position of my agent
        :param adv_pos: the position of the adversary agent
        :param max_step: the maximum number of steps

        :return: the heuristic value
        """ 
        max_number_of_valid_moves = 1 + 2 * max_step * (max_step + 1)

        return len(self.valid_moves_adv_after_move(chess_board, move, max_step, adv_pos)) / max_number_of_valid_moves
    
    def endgame_heuristic(self, chess_board, move, adv_pos, max_step):
        """
        Heuristic function for endgame by checking if given move ends the game and if winning or not (0 if doesn't end, difference between scores if ends) normalizing it by the maximum possible score difference
        :param chess_board: the current chess board
        :param my_pos: the position of my agent
        :param adv_pos: the position of the adversary agent
        :param max_step: the maximum number of steps

        :return: the heuristic value
        """

        new_board = self.move_in(chess_board, move)
        
        #check if move ends the game

        is_endgame, score_diff = self.check_endgame(new_board, move[0], adv_pos)

        if is_endgame:
            return (score_diff + 1) / 2
        else:
            return 1/2
    
    
    def block_endgame_heuristic(self, chess_board, move, adv_pos, max_step):
        new_board = self.move_in(chess_board, move)
        x, y = move[0]
    
        # Sum up the values in the direction dimension
        sum_barriers = np.sum(new_board[x, y])

        return (sum_barriers - 1) / 3
    
    #final heuristic function
    def combined_heuristic(self, chess_board, move, adv_pos, max_step):
        """
        Heuristic function for combining the four heuristic functions above
        :param chess_board: the current chess board
        :param my_pos: the position of my agent
        :param adv_pos: the position of the adversary agent
        :param max_step: the maximum number of steps

        :return: the heuristic value
        """

        return 0.2 * (1-self.chasing_adversary_heuristic(chess_board, move, adv_pos, max_step)) + 0.15 * (1-self.center_heuristic(chess_board, move, adv_pos, max_step)) + 0.25 * (1-self.blocking_adversary_heuristic(chess_board, move, adv_pos, max_step)) + 0.4 * (1-self.block_endgame_heuristic(chess_board, move, adv_pos, max_step)) + 0.4 * (self.endgame_heuristic(chess_board, move, adv_pos, max_step))
    
    #get the tree of possible moves at depth 2
    def get_tree(self, chess_board, my_pos, adv_pos, max_step):
        """
        Returns the tree of possible moves

        :param chess_board: the current chess board
        :param my_pos: the position of my agent
        :param adv_pos: the position of the adversary agent
        :param max_step: the maximum number of steps

        :return: the tree of possible moves
        """

        tree = {}
        valid_moves = self.all_valid_moves(chess_board, my_pos, max_step, adv_pos)
        for move in valid_moves:
            tree[move] = self.combined_heuristic(chess_board, move, adv_pos, max_step)

        return tree
    
    
    def minimax_decision(self, tree):
        """
        Returns the minimax decision of the move

        :param tree: the tree of possible moves

        :return: the minimax decision move
        """

        best_move = max(tree, key=tree.get)

        return best_move

        


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

        start_time = time.time()

        #get the best move from minimax decision (depth 1 so far)
        best_move = self.minimax_decision(self.get_tree(chess_board, my_pos, adv_pos, max_step))

        self.MOVE_NUMBER+=1
        time_taken = time.time() - start_time
        
        #print("My AI's turn took ", time_taken, "seconds.")
        #return the move with the maximum heuristic value
        return best_move
