from names import *
import random
import numpy as np
class Player:
    def __init__(self,row):
        self.stats=row.to_dict()
        self.stats['team_position']='Reserves'
        self.setPosition()
        

    def setPosition(self):
        if 'B' in self.stats['player_positions'].split(",")[0]:
            self.stats['player_positions']='Defender'
        if 'M' in self.stats['player_positions'].split(",")[0]:
            self.stats['player_positions']='Midfielder'
        for x in ['S','F','W']:
            if x in self.stats['player_positions'].split(",")[0]:
                self.stats['player_positions']='Attacker'
        
        pass
