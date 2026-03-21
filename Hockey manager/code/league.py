import random
from simulating_match import simulating_match

class league:
    def __init__(self, teams):
        self.teams = teams
        self.shedule = []
        self.current_match_index = 0
        self.regular_season_ended = False
        self.conference = self.split_into_conferences()

    def split_into_conferences(self):
        mid = len(self.teams)
        west = self.teams[:mid]
        east = self.teams[mid:]
        return {"west": west, "east": east}

    def generate_shedule(self,rounds=4):
        for i in range(len(self.teams)):
            for j in range(len(self.teams)):
                if i!=j:
                    for _ in range(rounds):
                        self.shedule.append((self.teams[i], self.teams[j]))
        random.shufle(self.shedule)
        self.current_match_index = 0
        self.regular_season_ended = False
        