from __future__ import absolute_import, division, print_function
import copy, random
from game import Game

MOVES = {0: 'up', 1: 'left', 2: 'down', 3: 'right'}
MAX_PLAYER, CHANCE_PLAYER = 0, 1

# Tree node. To be used to construct a game tree.
class Node:
    # Recommended: do not modify this __init__ function
    def __init__(self, state, player_type):
        self.state = (state[0], state[1])

        # to store a list of (direction, node) tuples
        self.children = []

        self.player_type = player_type

    # returns whether this is a terminal state (i.e., no children)
    def is_terminal(self):
        return len(self.children) == 0

# AI agent. Determine the next move.
class AI:
    # Recommended: do not modify this __init__ function
    def __init__(self, root_state, search_depth=3):
        self.root = Node(root_state, MAX_PLAYER)
        self.search_depth = search_depth
        self.simulator = Game(*root_state)

    # (Hint) Useful functions:
    # self.simulator.current_state, self.simulator.set_state, self.simulator.move

    # TODO: build a game tree from the current node up to the given depth
    def build_tree(self, node = None, depth = 0):
        if node is None:
            node = self.root

        if depth == 0:
            return

        self.simulator.set_state(*node.state)

        if node.player_type == MAX_PLAYER:
            for direction in MOVES:
                self.simulator.set_state(*node.state)
                if self.simulator.move(direction):
                    child = Node(self.simulator.current_state(), CHANCE_PLAYER)
                    node.children.append((direction, child))
                    self.build_tree(child, depth - 1)
        else:
            for tile in self.simulator.get_open_tiles():
                self.simulator.set_state(*node.state)
                self.simulator.tile_matrix[tile[0]][tile[1]] = 2
                child = Node(self.simulator.current_state(), MAX_PLAYER)
                node.children.append((None, child))
                self.build_tree(child, depth - 1)

    # TODO: expectimax calculation.
    # Return a (best direction, expectimax value) tuple if node is a MAX_PLAYER
    # Return a (None, expectimax value) tuple if node is a CHANCE_PLAYER
    def expectimax(self, node = None):
        if node is None:
            node = self.root

        if node.is_terminal():
            return None, node.state[1]

        if node.player_type == MAX_PLAYER:
            best_direction = None
            best_value = float("-inf")

            for direction, child in node.children:
                _, child_value = self.expectimax(child)
                if child_value > best_value:
                    best_direction = direction
                    best_value = child_value

            return best_direction, best_value

        total_value = 0
        for _, child in node.children:
            _, child_value = self.expectimax(child)
            total_value += child_value

        return None, total_value / len(node.children)

    # Return decision at the root
    def compute_decision(self):
        self.build_tree(self.root, self.search_depth)
        direction, _ = self.expectimax(self.root)
        return direction

    # TODO (optional): the extension part
    def compute_decision_extension(self):
        return random.randint(0, 3)
