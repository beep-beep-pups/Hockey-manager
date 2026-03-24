import random
from hockey_manager import load_teams_from_json, save_teams_to_json, team
from league import league
from transfers import transfer_market
from update_skills import end_of_season_update

def show_stats(team):
    print(f"\n Statistic {team.name} ===")
    print(f"Wins: ({team.wins}+{team.wins_ot}), Loses: ({team.loses}+{team.loses_ot})")
    print(f"Goal scored: {team.goal_scored}, Goal conceded: {team.goal_conceded}")
    print("Top scorer:")
    scored_players = sorted(team.players, key = lambda p: p.points, reverse=True)
    for p in scored_players[:3]:
        print(f" {p.name} - {p.points} points ({p.goals}+{p.assists})")
    
def choose_user_team(teams):
    print("Available teams:")
    for i, t in enumerate(teams, 1):
        print(f"{i} {t.name}")
    while True:
        try:
            choice = int(input("Select the team number, you want to play for: "))
            if 1 <= choice <= len(teams):
                return teams[choice-1]
            else:
                print("Incorrect number")
        except ValueError:
            print("Select number")

def main():
    all_teams = load_teams_from_json("teams.json")
    if not all_teams:
        print("Failed to load teams. Check the teams.json file")
        return
    
    user_team = choose_user_team(all_teams)
    league = league(all_teams)
    season_in_progress = False
    playoffs_in_progress = False
    user_tactic = "neutral"

    while True:
        print(f"\n=== HOCKEY MANAGER ===")
        print(f"Team: {user_team.name} | Budget: {user_team.budget} million rubles")
        print("1 Train management")
        print("2 Start/continue season")
        print("3 Tournament table")
        print("4 Choose tactic (now: " + user_tactic + ")")
        print("5 Save and exit")
        choice = input("Your choice: ").strip()

        if choice == "1":
            transfer_market(user_team, all_teams, playoffs_in_progress)
            save_teams_to_json(all_teams)
        
        elif choice == "2":
            if not season_in_progress and not playoffs_in_progress:
                for t in all_teams:
                    t.wins = t.wins_ot = t.loses = t.loses_ot = t.points = 0
                    t.goals_conceded = t.goals_scored = 0
                league.generate_shedule(rounds=4)
                league.current_round = 0
                season_in_progress = True
                print("New season started!")
            elif playoffs_in_progress:
                print("Playoff continue")
                continue

            user_report, season_ended = league.simulate_round(user_team)
            if user_report:
                print(user_report)
            else:
                print("Your team is not playing in this round")
            league.print_satandings()
            if season_ended:
                print("\nRegular season ended!")
                league.print_standings()
                print("\nPlayoff started")
                playoffs_in_progress = True
                champion = league.run_playoffs()
                if champion:
                    print(f"\nChampion: {champion.name}")

                end_of_season_update(all_teams)
                save_teams_to_json(all_teams)
                season_in_progress = False
                playoffs_in_progress = False
                print("\nSeason ended")
        elif choice == "3":
            league.print_standings()

        elif choice == "4":
            print("Choose tactic:")
            print("1 Aggressive")
            print("2 Neutral")
            print("3 Defensive")
            tac = input("Your choice:").strip()

            if tac == "1":
                user_tactic = "aggressive"
            elif tac == "2":
                user_tactic = "neutral"
            elif tac == "3":
                user_tactic = "defensive"
            else:
                print("Wrong choice, tactics have not been changed")
            print(f"New tactic: {user_tactic}")
            user_team.tactic = user_tactic
        elif choice == "5":
            save_teams_to_json(all_teams)
            break
        else:
            print("Choose correct number")

if __name__ == "__main__":
    main()
