def update_skiils(player):
    if player.games_played == 0:
        return
    if player.position == "Forward":
        avg_points = player.points / player.games_played
        expected_avg = player.skill / 20
        delta = avg_points - expected_avg
        skill_change = int(delta * 5)
    elif player.position == "Defender":
        avg_points = player.points / player.games_played
        expected_pts = player.skill / 25
        pts_delta = avg_points - expected_pts
        plus_minus_avg = player.plus_minus / player.games_played
        pm_delta = plus_minus_avg
        delta = 0.7 * pts_delta + 0.3 * pm_delta
        skill_change = int(delta * 5)
    else:
        total_shots = player.saves + player.goals.against
        if total_shots == 0:
            return
        save_pct = player.saves / total_shots
        expected_pct = 0.85 + (player.skill / 100) * 0.1
        delta = save_pct - expected_pct
        skill_change = int(delta * 100)

    new_skill = player.skill + skill_change
    new_skill = max(0, min(100, new_skill))
    player.skill = new_skill
    player.games_played = 0
    player.goals = 0
    player.assists = 0
    player.points = 0
    player.saves = 0
    player.goals_against = 0
    player.plus_minus = 0

def end_of_season_update(teams):
    for team in teams:
        for player in team.players:
            update_skiils(player)
    print("Players skills have been updated based on the results of the season")
