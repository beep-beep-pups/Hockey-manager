def show_stats(team):
    print(f"\n Statistic {team.name} ===")
    print(f"Wins: ({team.wins}+{team.wins_ot}), Loses: ({team.loses}+{team.loses_ot})")
    print(f"Goal scored: {team.goal_scored}, Goal conceded: {team.goal_conceded}")
    print("Top scorer:")
    scored_players = sorted(team.players, key = lambda p: p.points, reverse=True)
    for p in scored_players[:3]:
        print(f" {p.name} - {p.points} points ({p.goals}+{p.assists})")
    