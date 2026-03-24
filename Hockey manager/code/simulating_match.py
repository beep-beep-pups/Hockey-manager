import random
import math

def simulating_match(team1, team2, home_team=None, home_advantage=1.1, is_playoff = False):
    def team_attack_strength(team):
        field_players = [p for p in team.players if p.position != "Goalkeeper"]
        if not field_players:
            return 52
        strength = sum(p.skill for p in field_players) / len(field_players)
        return strength

    def save_probability(goalkeeper_skill):
        return 0.80 + (goalkeeper_skill / 100) * 0.1

    # Базовые силы атаки
    base_attack1 = team_attack_strength(team1)
    base_attack2 = team_attack_strength(team2)

    # Расчитываем коэффициенты тактики для атаки и защиты 
    def get_tactic_coeffs(team):
        tactic = getattr(team, 'tactic', 'neutral')
        if tactic == "aggressive":
            return 1.1, 1.1
        elif tactic == "defensive":
            return 0.9, 0.9
        else:
            return 1.0, 1.0

    attack_coeff1, defence_coeff1 = get_tactic_coeffs(team1)
    attack_coeff2, defence_coeff2 = get_tactic_coeffs(team2)

    # Модифицируем атаку для расчёта бросков и дополняем домашним преимуществом
    attack1_final = base_attack1 * attack_coeff1
    attack1_final *= (home_advantage if home_team == team1 else 1.0)
    attack2_final = base_attack2 * attack_coeff2
    attack2_final *= (home_advantage if home_team == team2 else 1.0)

    # Фактор рандома
    factor1 = random.uniform(0.9, 1.1)
    factor2 = random.uniform(0.9, 1.1)
    attack1 = attack1_final * factor1
    attack2 = attack2_final * factor2

    def select_goalie(team):
        goalies = [p for p in team.players if p.position == "Goalkeeper"]
        if len(goalies) == 1:
            return goalies[0]
        goalies_sorted = sorted(goalies, key = lambda g: g.skill, reverse=True)
        best = goalies_sorted[0]
        if random.random() < 0.8:
            return best
        else:
            return random.choice(goalies_sorted[1:])
        
    goalie1 = select_goalie(team1)
    goalie2 = select_goalie(team2)

    total_goals1 = 0
    total_goals2 = 0
    period_reports = []
    base_shots_per_period = 7
    shots_factor = 0.03

    for period in range(1, 4):

        # Ожидаемое количество бросков
        exp_shots1 = base_shots_per_period + (attack1 - 70) * shots_factor
        exp_shots2 = base_shots_per_period + (attack2 - 70) * shots_factor
        exp_shots1 = max(5, min(15, exp_shots1))
        exp_shots2 = max(5, min(15, exp_shots2))

        exp_shots1 *= defence_coeff2
        exp_shots2 *= defence_coeff1

        shots1 = int(random.poisson(exp_shots1))
        shots2 = int(random.poisson(exp_shots2))

        # Голы первой команды
        if goalie2:
            save_pct2 = save_probability(goalie2.skill)
            goals1 = int(shots1 * (1 - save_pct2) + random.gauss(0, 0.5))
            goals1 = max(0, min(shots1, goals1))
            goalie2.saves += (shots1 - goals1)
            goalie2.against_goals += goals1
        else:
            goals1 = shots1

        # Голы второй команды
        if goalie1:
            save_pct1 = save_probability(goalie1.skill)
            goals2 = int(shots2 * (1 - save_pct1) + random.gauss(0, 0.5))
            goals2 = max(0, min(shots2, goals2))
            goalie1.saves += (shots2 - goals2)
            goalie1.against_goals += goals2
        else:
            goals2 = shots2

        for _ in range(goals1):
            field = [p for p in team1.players if p.position != "Goalkeeper"]

            # Гол
            if field:
                scorer = random.choice(field)
                scorer.goals += 1
                scorer.points += 1

            # Ассист
            if random.random() < 0.8:
                possible_assistant = [p for p in field if p != scorer and p.position != "Goalkeeper"]
                if possible_assistant:
                    assistant = random.choice(possible_assistant)
                    assistant.assists += 1
                    assistant.points += 1
            for p in team1.players:
                if p.position != "Goalkeeper":
                    p.plus_minus += 1
            for p in team2.players:
                if p.position != "Goalkeeper":
                    p.plus_minus -=1

        for _ in range(goals2):
            field = [p for p in team2.players if p.position != "Goalkeeper"]

            # Гол
            if field:
                scorer = random.choice(field)
                scorer.goals += 1
                scorer.points += 1

            # Ассист
            if random.random() < 0.8:
                possible_assistant = [p for p in field if p != scorer and p.position != "Goalkeeper"]
                if possible_assistant:
                    assistant = random.choice(possible_assistant)
                    assistant.assists += 1
                    assistant.points += 1
            for p in team2.players:
                if p.position != "Goalkeeper":
                    p.plus_minus += 1
            for p in team1.players:
                if p.position != "Goalkeeper":
                    p.plus_minus -=1

        total_goals1 += goals1
        total_goals2 += goals2
        period_reports.append(
            f"{period} Period: \n"
            f"Team {team1.name}: {shots1} shots, {goals1} goals\n"
            f"Team {team2.name}: {shots2} shots, {goals2} goals"
        )

    ot_goals1 = 0
    ot_goals2 = 0
    shootout_score1 = 0
    shootout_score2 = 0
    win_type = None 
    winner = None

    # Овертайм
    if total_goals1 == total_goals2:
        if is_playoff:
            ot_period = 1
            while True:
                expected_ot_goals1 = attack1 / 400
                expected_ot_goals2 = attack2 / 400
                if expected_ot_goals1 > 0 or expected_ot_goals2 > 0:
                    u1 = random.random()
                    u2 = random.random()
                    if u1 == 0: u1 = 1e-10
                    if u2 == 0: u2 = 1e-10

                    time1 = -math.log(1 - u1) / expected_ot_goals1 if expected_ot_goals1 > 0 else float('inf')
                    time2 = -math.log(1 - u2) / expected_ot_goals2 if expected_ot_goals2 > 0 else float('inf')
                    
                    if time1 < time2:
                        ot_winner = team1
                        ot_goals = 1
                        win_type = "ot_playoff"
                        break
                    elif time2 < time1:
                        ot_winner = team2
                        ot_goals2 = 1
                        win_type = "ot_playoff"
                        break
                    else:
                        continue
                else:
                    if random.random() < 0.5:
                        winner = team1
                        ot_goals1 = 1
                    else:
                        winner = team2
                        ot_goals2 = 1
                    win_type = "ot_playoff"
                    break
                ot_period += 1
            total_goals1 += ot_goals1
            total_goals2 += ot_goals2
            period_reports.append(f"Overtime {ot_period}: {winner.name} score and win!")

        else:
            expected_ot_goals1 = attack1 / 240
            expected_ot_goals2 = attack2 / 240
            if expected_ot_goals1 > 0 or expected_ot_goals2 > 0:
                u1 = random.random()
                u2 = random.random()
                if u1 == 0: u1 = 1e-10
                if u2 == 0: u2 = 1e-10

                time1 = -math.log(1 - u1) / expected_ot_goals1 if expected_ot_goals1 > 0 else float('inf')
                time2 = -math.log(1 - u2) / expected_ot_goals2 if expected_ot_goals2 > 0 else float('inf')
                    
                if time1 < time2:
                    ot_winner = team1
                    ot_goals = 1
                elif time2 < time1:
                    ot_winner = team2
                    ot_goals2 = 1
                else:
                    ot_winner = None
            if ot_winner is not None:
                total_goals1 += ot_goals1
                total_goals2 += ot_goals2
                if ot_winner == team1:
                    field = [p for p in team1.players if p .position != "Goalkeeper"]
                    if field:
                        scorer = random.choice(field)
                        scorer.goals += 1
                        scorer.points += 1
                    win_type = "ot"
                    winner = team1
                    period_reports.append(f"Overtime: {team1.name} score goal and win")
                else:
                    field = [p for p in team2.players if p .position != "Goalkeeper"]
                    if field:
                        scorer = random.choice(field)
                        scorer.goals += 1
                        scorer.points += 1
                    win_type = "ot"
                    winner = team2
                    period_reports.append(f"Overtime: {team2.name} score goal and win")
            else:
                win_type = "shootout"
                period_reports.append(f"The overtime ended with no goals. Shootout series")

            # Буллиты
            skaters1 = [p for p in team1.players if p.position != "Goalkeeper"]
            skaters2 = [p for p in team2.players if p.position != "Goalkeeper"]
            
            # Копии для использования
            available1 = skaters1.copy()
            available2 = skaters2.copy()
            attempt = 0
            shootout_report = []

            def shootout_prob(shooter, goalie):
                prob = 0.3 + (shooter.skill - (goalie.skill if goalie else 50)) / 200
                return max(0.05, min(0.7, prob))
            for _ in range(5):
                if not available1:
                    available1 = skaters1.copy()
                if not available2:
                    available2 = skaters2.copy()
                
                shooter1 = random.choice(available1)
                shooter2 = random.choice(available2)
                available1.remove(shooter1)
                available2.remove(shooter2)

                goal1 = random.random() < shootout_prob(shooter1, goalie2)
                goal2 = random.random() < shootout_prob(shooter2, goalie1)

                if goal1:
                    shootout_score1 += 1
                if goal2:
                    shootout_score2 += 1
                
                shootout_report.append(
                    f"(shooter1.name) - {'score' if goal1 else 'not score'}"
                    f"(shooter2.name) - {'score' if goal2 else 'not score'}"
                )
                shootout_round += 1
            while shootout_score1 == shootout_score2:
                if not available1:
                    available1 = skaters1.copy()
                if not available2:
                    available2 = skaters2.copy()
                shooter1 = random.choice(available1)
                shooter2 = random.choice(available2)
                available1.remove(shooter1)
                available2.remove(shooter2)

                goal1 = random.random() < shootout_prob(shooter1, goalie2)
                goal2 = random.random() < shootout_prob(shooter2, goalie1)
                if goal1:
                    shootout_score1 += 1
                if goal2:
                    shootout_score2 += 1
                shootout_round += 1
                shootout_report.append( 
                    f"{shootout_round}: {shooter1.name} – {'score' if goal1 else 'not score'}, " 
                    f"{shooter2.name} – {'score' if goal2 else 'not score'}"
                )
                if goal1 != goal2:
                    break

            winner = team1 if shootout_score1 > shootout_score2 else team2
            period_reports.append("Shootout:")
            period_reports.extend(shootout_report)
            period_reports.append(f"The result of the shootout series: {shootout_score1}:{shootout_score2} - {winner.name} win") 
            
    if win_type is None:
        if total_goals1 > total_goals2:
            winner = team1
            win_type = "regulation"
        else:
            winner = team2
            win_type = "regulation"
    
    if not is_playoff:
        if win_type == "regulation":
            if winner == team1:
                team1.wins += 1
                team2.loses += 1
            else:
                team2.wins += 1
                team1.loses += 1
        elif win_type == "ot":
            if winner == team1:
                team1.wins_ot += 1
                team2.loses_ot += 1
            else:
                team2.wins_ot += 1
                team1.loses_ot += 1
        elif win_type == "shootout":
            if winner == team1:
                team1.wins_ot += 1
                team2.loses_ot += 1
            else:
                team2.wins_ot += 1
                team1.loses_ot += 1
    
    for p in team1.players:
        p.games_played += 1
    for p in team2.players:
        p.games_played += 1

    team1.goals_scored += total_goals1
    team1.goals_conceded += total_goals2
    team2.goals_scored += total_goals2
    team2.goals_conceded += total_goals1

    if win_type == "regulation":
        result_text = f"{winner.name} win"
    elif win_type == "ot":
        result_text = f"{winner.name} win in overtime"
    elif win_type == "ot_playoff":
        result_text = f"{winner.name} win in playoff overtime"
    else:
        result_text = f"{winner.name} win in shootout series"

    full_report = f"{team1.name} {total_goals1} : {total_goals2} {team2.name} – {result_text}\n"
    full_report += "\n".join(period_reports)

    return{
            "winner": winner,
            "win_type": win_type,
            "score": (total_goals1, total_goals2),
            "ot_goals": (ot_goals1, ot_goals2),
            "shootout_score": (shootout_score1, shootout_score2),
            "report": full_report
        }
