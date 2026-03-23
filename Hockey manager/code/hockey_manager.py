import json

class player:
    def __init__(self, name, position, skill, price):
        self.name = name
        self.position = position
        self.skill = skill
        self.price = price  
        self.games_played = 0
        self.goals = 0
        self.assists = 0
        self.points = 0
        self.saves = 0
        self.goals_against = 0
        self.plus_minus = 0
    def __repr__(self):
        return f"{self.name} ({self.position}) – скилл: {self.skill}, очки: {self.points} (г: {self.goals}, п: {self.assists})"
    
    def to_dict(self):
        return{
            "name": self.name,
            "position": self.position,
            "skill": self.skill,
            "price": self.price,
            "games_played": self.games_played,
            "goals": self.goals,
            "assists": self.assists,
            "points": self.points,
            "saves": self.saves,
            "goals_against": self.goals_against,
            "plus_minus": self.plus_minus
        }
        
    @staticmethod
    def from_dict(data):
        p=player(data["name"], data["position"], data["skill"],data.get("price"))
        p.games_played = data.get("games_played", 0)
        p.goals = data.get("goals", 0)
        p.assists = data.get("assists", 0)
        p.points = data.get("points", 0)
        p.saves = data.get("saves", 0)
        p.goals_against = data.get("goals_against", 0)
        return p
    
class team:
    def __init__(self,name,budget):
        self.name = name
        self.players = []
        self.budget = budget
        self.wins = 0
        self.wins_ot = 0
        self.loses = 0
        self.loses_ot = 0
        self.points = 0
        self.goals_scored = 0
        self.goals_conceded = 0
        self.playoff_wins = 0
        self.tactic = "neutral"

    def add_player(self, player):
        self.players.append(player)

    def remove_player(self, player):
        if player in self.players:
            self.players.remove(player)

    def team_strength(self):
        if not self.players:
            return 0
        return sum(p.skill for p in self.players) / len(self.players)
    
    def show_roster(self):
            print(f"\nTeam roster {self.name}:")
            for i, player in enumerate(self.players, 1):
                print(f"{i}. {player}")
    
    def to_dict(self):
        return {
            "name": self.name,
            "budget": self.budget,
            "players": [p.to_dict() for p in self.players],
            "wins": self.wins,
            "wins_ot": self.wins_ot,
            "loses": self.loses,
            "loses_ot": self.loses_ot,
            "points": self.points,
            "goals_scored": self.goals_scored,
            "goals_conceded": self.goals_conceded
        }
    
    @staticmethod
    def from_dict(data):
        team = team(data["name"], data.get("budget"))
        for p_data in data["players"]:
            team.add_player(player.from_dict(p_data))
        team.wins = data.get("wins", 0)
        team.wins_ot = data.get("wins_ot", 0)
        team.loses = data.get("loses", 0)
        team.loses_ot = data.get("loses_ot", 0)
        team.points = data.get("points", 0)
        team.goals_scored = data.get("goals_scored", 0)
        team.goals_conceded = data.get("goals_conceded", 0)
        return team

def load_teams_from_json(filename = "teams.json"):
    with open(filename, "r", encoding = "utf-8") as f:
        data = json.load(f)
    teams = []
    for t_data in data:
        teams.append(team.from_dict(t_data))
    return teams

def save_teams_to_json(teams, filename = "teams.json"):
    data = [t.to_dict() for t in teams]
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii = False, indent = 4)
