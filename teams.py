import pprint as pp
import players as p
from manager import *
from names import gen_name
import numpy as np
import random
import pandas as pd
from playerlist import df
from tabulate import tabulate

class Team:
    attlist=['long_name','nationality', 'overall', 'player_positions','team_position', 'pace','shooting', 'passing', 'dribbling', 'defending', 'physical']
    def __init__(self,team_name):
        self.players={}
        self.squad={}
        self.subs={}
        self.reserves={}
        self.team_name=team_name
        self.addPlayers()
        self.attackers={}
        self.midfielders={}
        self.defenders={}
        self.goalkeepers={}   
        self.populatePositions()
        self.manager=None
        self.setManager()
        self.playingSquad()
        self.attack=round(np.array([a.stats['overall'] for a in self.players.values() if a.stats['player_positions']=='Attacker' and (a.stats['team_position']=='Starter' or a.stats['team_position']=='Substitute')]).mean())
        self.midfield=round(np.array([a.stats['overall'] for a in self.players.values() if a.stats['player_positions']=='Midfielder' and (a.stats['team_position']=='Starter' or a.stats['team_position']=='Substitute')]).mean())
        self.defence=round(np.array([a.stats['overall'] for a in self.players.values() if (a.stats['player_positions']=='Defender' or a.stats['player_positions']=='GK') and (a.stats['team_position']=='Starter' or a.stats['team_position']=='Substitute')]).mean())
        # self.playingSquad()

    def addPlayers(self):
        tdf=df[df['club']==self.team_name]
        for index, row in tdf.iterrows():
            self.players[row['long_name']]=p.Player(row)
            pass



    def setManager(self):
        self.manager=Manager()

    def showPlayers(self,player_dict=None):
        if player_dict==None:
            player_dict=self.players
        pl=[]
        df=pd.DataFrame()
        i=1
        for player in player_dict.values():
            temp=pd.DataFrame.from_records(player.__dict__,index=[i],columns=Team.attlist)
            df=df.append(temp)
            i+=1
        print(tabulate(df,headers=[c.capitalize() for c in df.columns],tablefmt='psql',stralign='left'))
            
    
    def populatePositions(self):
        for player in self.players.values():
            if player.stats['player_positions'] =='Attacker':
                self.attackers[player.stats['long_name']]=player
            if player.stats['player_positions'] =='Defender':
                self.defenders[player.stats['long_name']]=player
            if player.stats['player_positions'] =='Midfielder':
                self.midfielders[player.stats['long_name']]=player
            if player.stats['player_positions'] =='GK':
                self.goalkeepers[player.stats['long_name']]=player

    def showManager(self):
        table_data=[]
        table_data.append([self.manager.stats['long_name'],'Manager',self.manager.stats,self.manager.ivs,self.manager.formation])
        print(tabulate(table_data))

    def showTeam(self,player_dict=None,position=['striker','midfielder','defender','goalkeeper']):
        self.Substitutes()
        self.showPlayers()
        self.showPlayers(player_dict=self.squad)
        self.showStats()
        self.showManager()


    def showStats(self):
        print(f"{self.team_name}'s Stats\nAttack = {self.attack}\nMidfield = {self.midfield}\nDefence = {self.defence}")
        
    def playingSquad(self):
        squad={}
        attackers=list(self.attackers.values())
        attackers.sort(key = lambda x:x.stats['overall'],reverse=True)
        for player in attackers[0:self.manager.strikers]:
            player.stats['team_position']='Starter'
            squad[player.stats['long_name']]=player

        midfielders=list(self.midfielders.values())
        midfielders.sort(key = lambda x:x.stats['overall'],reverse=True)
        for player in midfielders[0:self.manager.midfielders]:
            player.stats['team_position']='Starter'
            squad[player.stats['long_name']]=player

        defenders=list(self.defenders.values())
        defenders.sort(key = lambda x:x.stats['overall'],reverse=True)
        for player in defenders[0:self.manager.defenders]:
            player.stats['team_position']='Starter'
            squad[player.stats['long_name']]=player

        goalkeepers=list(self.goalkeepers.values())
        goalkeepers.sort(key = lambda x:x.stats['overall'],reverse=True)
        goalkeepers[0].stats['team_position']='Starter'
        squad[goalkeepers[0].stats['long_name']]=goalkeepers[0]
        self.squad=squad

    def Substitutes(self):
        subs=[x for x in self.players.keys() if x not in self.squad.keys()][:7]
        for player in subs:
            self.players[player].stats['team_position']='Substitute'
            self.subs[player]=self.players[player]
        reserves = [r for r in self.players.items() if (r not in self.squad.items() and r not in self.subs.items())]
        self.reserves.update(reserves)
        pass
