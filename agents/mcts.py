import time
import math
import numpy as np
import random

def uct(node):
    return node.wins / node.visits + 2 * math.sqrt(math.log(node.parent.visits) / node.visits)

def random_child_expansion_policy(node):
  return node.unvisited_children_states.pop(random.randrange(len(node.unvisited_children_states)))

def random_simulation(state, generate_children, utility, simulation_depth):
  children = generate_children(state)
  while simulation_depth > 0 and children != []:
    state = random.choice(children)
    children = generate_children(state)
    simulation_depth -= 1
  return utility(state)


class MCTS():
  """
  Monte Carlo Tree Search
        - Selection 
              - find the most promising node
              - if node is not fully expanded, expand it
              - if it is expanded keep selecting until a leaf node is reached
              - Promising means that it has a high value and has not been explored much
              - formula: UCT = V + C * sqrt(ln(N) / n)
                - V = value of node
                - C = exploration parameter
                - N = number of times parent node has been visited
                - n = number of times child node has been visited
        - Expansion
              - If not expanded, select some amount of children to expand
        - Simulation
              - Run a simulation from the selected node to a certain depth
              - typically a random simulation where moves are chosen randomly
              - can also use a heuristic to guide the simulation
              - if we dont reach the end of the game, we need to evaluate the simulation or restart the simulation
              - we can evaluate using a utility function for the board
        - Backpropagation
              - use the result (win or loss) of the simulation to update the nodes
              - the nodes we need to update are the nodes that were visited during selection
              - update the value of the nodes by adding the result of the simulation to the value of the node
              - update the number of visits of the nodes by adding 1 to the number of visits of the node


  
  """

  def get_next_move(
      generate_children,
      utility,
      state,
      max_depth,
      simulation_depth,
      simulation_policy = random_simulation,
      child_expansion_policy = random_child_expansion_policy,
      time_limit = 2,
      memory_limit = 500, # in MB
      iterations = 1000
      ):
    
    """
    Function conditions:
    - generate_children: should return an empty list if the state is terminal
    - utilility: should return a value between -1 and 1, the utility function, 
        should be different for final game state and intermediate game states
        in the final game state, we want to return 1 if we won, -1 if we lost, and note use the heuristic
        in the intermediate game states, we want to return the heuristic value of the board

    - child_expansion_policy: needs to select and return a single child, and remove it from the list of unvisited children

    """
    
      #===========================================================================
    class Node():
      def __init__(self, state, parent=None):
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0
        self.unvisited_children_states = generate_children(state)
        self.state = state
      
      def is_terminal_node(self):
        return len(self.unvisited_children) + len(self.children) == 0
        

      def update(self, result):
        self.wins += result
        self.visits += 1
      
      def select_traversal_child(self):
        # if the node is the last node or if it has unvisited children, return None
        return self.children[np.argmax(map(uct, self.children))]
      
      
      def add_child(self, child):
        new_child = Node(child, self)
        self.children.append(new_child)
        return new_child
      #===========================================================================
    
    prev_time = time.time()
    def resouces_left():
      nonlocal iterations
      nonlocal time_limit
      nonlocal prev_time
      time_limit -= time.time() - prev_time
      prev_time = time.time()
      return iterations > 0 and time_limit > 0
    
    def selection(node):
      # we want to keep going until we encounter a leaf node, ie a terminal node
      # or, until we encounter a node that has unvisited children
      # so we want keep searching as long as our current not has no unvisited children and is not a terminal node
      while not node.is_terminal_node() and node.unvisited_children_states == []:
        node = node.select_traversal_child()
      return node

    def expansion(node):
      if node.unvisited_children_states == []:
        return
      # choose a child to expand
      # the expansion policy is responsible for removing the child from the list of unvisited children
      new_child = node.add_child( child_expansion_policy(node) )
      return new_child

    def backpropagation(node, result):
      while node != None:
        node.update(result)
        node = node.parent
      return node
    
    def mcts(root):
      
      node = root
      
      while resouces_left():
        iterations -= 1
        
        node = selection(node)
        new_child_node = expansion(node)
        result = simulation_policy(new_child_node.state, generate_children, utility, simulation_depth)
        node = backpropagation(node, result)
      
      return root.select_traversal_child().state

    root = Node(state, None, generate_children(state))
    return mcts(root)

    


    
    
