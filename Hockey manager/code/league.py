import random
from simulating_match import simulating_match

class league:
    def __init__(self, teams):
        self.teams = teams
        self.shedule_by_rounds = []
        self.current_round = 0
        self.conferences = self.split_into_conferences()

    def split_into_conferences(self):
        mid = len(self.teams) // 2
        west = self.teams[:mid]
        east = self.teams[mid:]
        return {"west": west, "east": east}

    def generate_shedule(self,rounds=4):
        self.shedule_by_rounds = []
        first_circle = self._round_robin(self.teams)
        second_circle = self._reverse_round_robin(first_circle)

        for _ in range(rounds // 2):
            self.shedule_by_rounds.extend(first_circle)
            self.shedule_by_rounds.extend(second_circle)
        if rounds % 2 == 1:
            self.shedule_by_rounds.extend(first_circle)

    def _round_robin(self, teams):
        n = len(teams)
        if n % 2 != 0:
            teams = teams + [None]
            n += 1
        else:
            teams = teams.copy()
        
        shedule = []
        fixed = teams[0]
        rotating = teams[1:]

        for _ in range(n-1):
            round_matches = []
            if rotating[0] is not None and fixed is not None:
                round_matches.append((fixed,rotating[0]))
            for j in range(1, n//2):
                home = rotating[j]
                away = rotating[n - 1 - j]
                if home is not None and away is not None:
                    round_matches.append((home,away))
            shedule.append(round_matches)
            rotating = [rotating[0]] + [rotating[-1]] + rotating[1:-1]
        return shedule
            
    def _reverse_round_robin(self,first_circle):
        reverse = []
        for round_matches in first_circle:
            reverse_round = [(away, home) for home, away in round_matches]
            reverse.append(reverse_round)
        return reverse
    
    def get_current_user_match(self, user_team):
        if self.current_round >= len(self.shedule_by_rounds):
            return None
        for home, away in self.shedule_by_rounds[self.current_round]:
            if home == user_team or away == user_team:
                return (home, away)
        return None
    
    def simulate_round(self, user_team):
        if self.current_round >= len(self.shedule_by_rounds):
            return "Season is over", True
        
        round_matches = self.shedule_by_rounds[self.current_round]
        user_report = None
        for home, away in round_matches:
            result = simulating_match(home, away, home_team = home)
            if (home == user_team or away == user_team) and user_report is None:
                user_report = result["report"]

        self.current_round += 1
        season_ended = (self.current_round >= len(self.shedule_by_rounds))
        return user_report, season_ended
    
    def get_standings(self, conference=None):
        if conference:
            teams_subset = self.conferences[conference]
        else:
            teams_subset = self.teams
        return sorted(teams_subset,
                      key= lambda t: (t.points, t.goals_scored - t.goals.conceded), reverse = True)
    
    def print_standings(self, conference=None):
        if conference:
            title = f"CONFERENCE ROUND-ROBIN TABLE {conference.upper()}"
            teams = self.get_standings(conference)
        else:
            title = "TOURNAMENT TABLE"
            teams = self.get_standings()
        print(f"\n=== {title} ===")
        print(f"{'Team':<15} {'M':<3} {'W':<3} {'WО':<3} {'L':<3} {'LО':<3} {'P':<3} {'G':<5}")
        for team in teams:
            games = team.wins + team.wins_ot + team.loses + team.loses_ot
            print(f"{team.name:<15} {games:<3} {team.wins:<3} {team.wins_ot:<3} "
                  f"{team.loses:<3} {team.loses_ot:<3} {team.points:<3} "
                  f"{team.goals_scored}-{team.goals_conceded}")
    
    def determine_playoff_teams(self):
        playoff_teams = []
        for conf in ["west","east"]:
            conf_teams = self.get_standings(conf)
            playoff_teams[conf] = conf_teams[:8]
        return playoff_teams
    
    def simulate_playoff_series(self, team1, team2, wins_needed = 4):
        team1.playoff_wins = 0
        team2.playoff_wins = 0
        games_log = []
        game_num = 1
        
        while team1.playoff_wins < wins_needed and team2.playoff_wins < wins_needed:
            if (game_num == 1) or (game_num == 2) or (game_num == 5) or (game_num == 7):
                home = team1
            else:
                home = team2
            result = simulating_match(team1, team2, home_team = home)
            games_log.append(result["report"])
            if result["winner"] == team1:
                team1.playoff_wins += 1
            else:
                team2.playoff_wins += 1
            game_num += 1
        winner = team1 if team1.playoff_wins == wins_needed else team2
        return winner, games_log
    
    def show_playoff_bracket(self, playoff_teams):
        print("\n=== Playoff ===")
        for conf in ["west", "east"]:
            print(f"\nСonference {conf.upper()}:")
            teams = playoff_teams[conf]
            print(f"1. {teams[0].name} - {teams[7].name}")
            print(f"1. {teams[1].name} - {teams[6].name}")
            print(f"1. {teams[2].name} - {teams[5].name}")
            print(f"1. {teams[3].name} - {teams[4].name}")

    def run_playoffs(self):
        playoff_teams = self.determine_playoff_teams()
        if len(playoff_teams["west"]) < 8 or len(playoff_teams["east"]) < 8:
            print("Teams not enough")
            return None
        
        self.show_playoff_bracket(playoff_teams)
        
        quarter_qualifiers = {"west": [], "east": []}
        for conf in ["west","east"]:
            print(f"\n=== Playoff conference {conf.upper()} ===")
            teams = playoff_teams[conf]
            pairs = [
                (teams[0], teams[7]), (teams[1],teams[6]), (teams[2], teams[5]), (teams[3], teams[4])
            ]
            winners = []
            for seed, (t1,t2) in enumerate(pairs, start =1):
                print(f"\nROUND OF 16 ({seed}): {t1.name} vs {t2.name}")
                winner, games = self.simulate_playoff_series(t1,t2)
                print(f"Series winner: {winner.name}")
                for g in games:
                    print(g)
                winners.append((seed, winner))
            quarter_qualifiers[conf] = winners

        west1 = next(t for seed, t in quarter_qualifiers["west"] if seed == 1)
        west2 = next(t for seed, t in quarter_qualifiers["west"] if seed == 2)
        west3 = next(t for seed, t in quarter_qualifiers["west"] if seed == 3)
        west4 = next(t for seed, t in quarter_qualifiers["west"] if seed == 4)

        east1 = next(t for seed, t in quarter_qualifiers["east"] if seed == 1)
        east2 = next(t for seed, t in quarter_qualifiers["east"] if seed == 2)
        east3 = next(t for seed, t in quarter_qualifiers["east"] if seed == 3)
        east4 = next(t for seed, t in quarter_qualifiers["east"] if seed == 4)

        group_a_pairs = [
            (west1, east4),
            (west2, east3)
        ]
        group_b_pairs = [
            (west3, east2),
            (west4, east1)
        ]

        group_winners = {"A": [], "B": []}
        print("\n=== QUARTERFINALS ===")
        for group_name, pairs in [("A", group_a_pairs), ("B", group_b_pairs)]:
            print(f"\nGroup {group_name}")
            for idx, (t1,t2) in enumerate(pairs, 1):
                print(f"\nRound of 8 (group {group_name}, match {idx}): {t1.name} vs {t2.name}")
                winner, games = self.simulate_playoff_series(t1,t2)
                print(f"Series winner: {winner.name}")
                for g in games:
                    print(g)
                group_winners[group_name].append(winner)

        print("\n=== SEMIFINALS ===")
        finalists = []
        for group_name in ["A","B"]:
            if len(group_winners[group_name]) == 2:
                t1, t2 = group_winners[group_name][0], group_winners[group_name][1]
                print(f"\nSemifinal (group {group_name}): {t1.name} vs {t2.name}")
                winner, games = self.simulate_playoff_series(t1,t2)
                print(f"Series winner: {winner.name}")
                for g in games:
                    print(g)
                finalists.append(winner)
        
        if len(finalists) == 2:
            print("\n=== FINAL OF THE GAGARIN CUP")
            champion, games = self.simulate_playoff_series(finalists[0],finalists[1])
            print(f"Champion: {champion.name}")
            for g in games:
                print(g)
            return champion
        else:
            return None
