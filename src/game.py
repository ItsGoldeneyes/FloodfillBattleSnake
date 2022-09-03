from standard_move import StandardMove
from board import Board
import random


class Game:
    def __init__(self, data):
        self.game_id = data["game"]["id"]
        self.self_id = data["you"]["id"]
        self.map = data["game"]["map"]
        self.rules = data["game"]["ruleset"]["name"]
        self.board = Board(data)
        
        self.possible_moves = ["up", "down", "left", "right"]
        
    def get_id(self):
        return self.game_id
    
    def get_rules(self):
        return self.board.get_rules()
    
    def get_snakes(self):
        return self.board.snakes

    def turn(self, data):
        self.board = Board(data)
        
        if self.rules == "standard" or "solo":
            move_type = StandardMove(self.board)
            move = move_type.choose_move(self.board.snakes[self.board.get_self_id()], depth= 1)
            
        else:
            potential_moves = self.board.find_moves(self.get_head())
            alive_moves = {move : potential_moves[move] for move in potential_moves if self.board.collision_check(potential_moves[move])==False}
            if alive_moves == {}:
                return "up"
            if self.board.get_health(self.id) < 30:
                food_dists = self.board.food_dist(self.get_head(), alive_moves)
                move_choice = min(food_dists, key=food_dists.get)
            else:
                move_choice = random.choice(list(alive_moves.keys()))
            move = move_choice
        
        if move in self.possible_moves and move != None:
            return move
        else:
            print("INCORRECT MOVE FORMAT:", move)
            return "up"