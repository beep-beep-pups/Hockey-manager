import random

def simulating_match(team1, team2, home_team=None, home_advantage=1.05):
    def team_attack_strength(team):
        """Средний скилл полевых игроков."""
        field_players = [p for p in team.players if p.position != "Goalkeeper"]
        if not field_players:
            return 52
        return sum(p.skill for p in field_players) / len(field_players)

    def save_probability(goalkeeper_skill):
        """Вероятность сейва вратаря."""
        return 0.80 + (goalkeeper_skill / 100) * 0.10

    def award_goal(team, is_ot=False, is_shootout=False):
        """Начисляет гол случайному полевому игроку и (с вероятностью 80%) ассист."""
        field_players = [p for p in team.players if p.position != "Goalkeeper"]
        if not field_players:
            return
        scorer = random.choice(field_players)
        scorer.goals += 1
        scorer.points += 1
        # Ассист
        if random.random() < 0.8:
            possible_assist = [p for p in team.players if p != scorer and p.position != "Goalkeeper"]
            if possible_assist:
                assistant = random.choice(possible_assist)
                assistant.assists += 1
                assistant.points += 1

    # ---------- Базовая сила атаки ----------
    base_attack1 = team_attack_strength(team1)
    base_attack2 = team_attack_strength(team2)

    # Поправка на домашнюю/гостевую игру
    attack_plus1 = base_attack1 + (home_advantage if home_team == team1 else 0.95)
    attack_plus2 = base_attack2 + (home_advantage if home_team == team2 else 0.95)

    # Фактор рандома
    factor1 = random.uniform(0.9, 1.1)
    factor2 = random.uniform(0.9, 1.1)
    attack1 = attack_plus1 + factor1
    attack2 = attack_plus2 + factor2

    # Вратари
    goalie1 = next((p for p in team1.players if p.position == "Goalkeeper"), None)
    goalie2 = next((p for p in team2.players if p.position == "Goalkeeper"), None)

    # ---------- Регулярное время (3 периода) ----------
    reg_goals1 = 0
    reg_goals2 = 0
    period_reports = []

    for period in range(1, 4):
        # Ожидаемое количество бросков
        base_shots = 7
        shots_factor = 0.04
        exp_shots1 = base_shots + (attack1 - 70) * shots_factor
        exp_shots2 = base_shots + (attack2 - 70) * shots_factor
        exp_shots1 = max(5, min(15, exp_shots1))
        exp_shots2 = max(5, min(15, exp_shots2))

        shots1 = int(random.poisson(exp_shots1))
        shots2 = int(random.poisson(exp_shots2))

        # Голы команды 1 (против вратаря 2)
        if goalie2:
            save_pct2 = save_probability(goalie2.skill)
            goals1 = int(shots1 * (1 - save_pct2) + random.gauss(0, 0.5))
            goals1 = max(0, min(shots1, goals1))
            goalie2.saves += (shots1 - goals1)
            goalie2.against_goals += goals1
        else:
            goals1 = shots1

        # Голы команды 2 (против вратаря 1)
        if goalie1:
            save_pct1 = save_probability(goalie1.skill)
            goals2 = int(shots2 * (1 - save_pct1) + random.gauss(0, 0.5))
            goals2 = max(0, min(shots2, goals2))
            goalie1.saves += (shots2 - goals2)
            goalie1.against_goals += goals2
        else:
            goals2 = shots2

        reg_goals1 += goals1
        reg_goals2 += goals2

        # Начисление голов и ассистов в регулярное время
        for _ in range(goals1):
            award_goal(team1, is_ot=False)
        for _ in range(goals2):
            award_goal(team2, is_ot=False)

        period_reports.append(
            f"{period}: {team1.name} – {shots1} shots, {goals1} goals; "
            f"{team2.name} – {shots2} shots, {goals2} goals"
        )

    total_goals1 = reg_goals1
    total_goals2 = reg_goals2
    ot_goals1 = 0
    ot_goals2 = 0
    shootout_score1 = 0
    shootout_score2 = 0
    result_text = ""
    win_type = None 

    # ---------- Овертайм (если ничья) ----------
    if reg_goals1 == reg_goals2:
        def ot_goal_probability(attack, goalie_skill):
            base = 0.08
            return max(0.02, min(0.3,
                        base + (attack - 70) / 500 - (goalie_skill - 80) / 500))

        prob1 = ot_goal_probability(attack1, goalie2.skill if goalie2 else 50)
        prob2 = ot_goal_probability(attack2, goalie1.skill if goalie1 else 50)

        max_attempts = 30
        ot_goal_scored = False
        for _ in range(max_attempts):
            scored1 = random.random() < prob1
            scored2 = random.random() < prob2
            # В овертайме может забить только одна команда
            if scored1 and scored2:
                if random.random() < 0.5:
                    scored2 = False
                else:
                    scored1 = False
            if scored1:
                ot_goals1 += 1
                award_goal(team1, is_ot=True)
                total_goals1 += 1
                result_text = f"{team1.name} win in overtime"
                win_type = "ot"
                ot_goal_scored = True
                break
            if scored2:
                ot_goals2 += 1
                award_goal(team2, is_ot=True)
                total_goals2 += 1
                result_text = f"{team2.name} win in overtime"
                win_type = "ot"
                ot_goal_scored = True
                break

        if not ot_goal_scored:
            # Переход к буллитам
            win_type = "shootout"
            result_text = f"Win in shootout series"
            period_reports.append("The overtime ended with no goals. Shootout series")

            # ---------- Серия буллитов ----------
            skaters1 = [p for p in team1.players if p.position != "Goalkeeper"]
            skaters2 = [p for p in team2.players if p.position != "Goalkeeper"]
            # Копии для использования (каждый может бить несколько раз)
            available1 = skaters1.copy()
            available2 = skaters2.copy()
            attempt = 0
            shootout_report = []
            # Стандартная серия – до 5 попыток
            while True:
                attempt += 1
                if not available1:
                    available1 = skaters1.copy()
                if not available2:
                    available2 = skaters2.copy()
                shooter1 = random.choice(available1)
                shooter2 = random.choice(available2)
                available1.remove(shooter1)
                available2.remove(shooter2)

                # Вероятность забить в буллитах
                def shootout_prob(shooter, goalie):
                    prob = 0.3 + (shooter.skill - (goalie.skill if goalie else 50)) / 200
                    return max(0.05, min(0.7, prob))

                goal1 = random.random() < shootout_prob(shooter1, goalie2)
                goal2 = random.random() < shootout_prob(shooter2, goalie1)

                if goal1:
                    shootout_score1 += 1
                    # В буллитах гол засчитывается, но не влияет на статистику вратарей и игроков
                if goal2:
                    shootout_score2 += 1

                shootout_report.append(
                    f"{shooter1.name} – {'забил' if goal1 else 'не забил'}, "
                    f"{shooter2.name} – {'забил' if goal2 else 'не забил'}"
                )

                # Условия завершения серии
                if attempt >= 5:
                    if abs(shootout_score1 - shootout_score2) >= 1:
                        break
                elif attempt >= 3 and abs(shootout_score1 - shootout_score2) > (5 - attempt):
                    break

            # Определение победителя буллитов
            if shootout_score1 > shootout_score2:
                winner = team1
                loser = team2
            else:
                winner = team2
                loser = team1

            # Запись победы по буллитам в ot_wins / loses_ot
            winner.wins_ot += 1
            winner.points += 2
            loser.loses_ot += 1
            loser.points += 1

            # Добавляем отчёт о буллитах
            period_reports.append("Серия буллитов:")
            period_reports.extend(shootout_report)
            period_reports.append(f"Итог буллитов: {shootout_score1}:{shootout_score2} – победил {winner.name}")

            # В случае буллитов общий счёт матча остаётся ничейным (по правилам хоккея)
            total_goals1 = reg_goals1
            total_goals2 = reg_goals2
        else:
            # Победа в овертайме: начисляем очки
            if ot_goals1 > 0:
                team1.wins_ot += 1
                team1.points += 2
                team2.loses_ot += 1
                team2.points += 1
            else:
                team2.wins_ot += 1
                team2.points += 2
                team1.loses_ot += 1
                team1.points += 1
    else:
        # Победа в основное время
        if reg_goals1 > reg_goals2:
            team1.wins += 1
            team1.points += 2
            team2.loses += 1
            result_text = f"{team1.name} win"
        else:
            team2.wins += 1
            team2.points += 2
            team1.loses += 1
            result_text = f"{team2.name} win"
        win_type = "regulation"

    # ---------- Общая статистика команд ----------
    team1.goals_scored += total_goals1
    team1.goals_conceded += total_goals2
    team2.goals_scored += total_goals2
    team2.goals_conceded += total_goals1

    # Увеличиваем количество сыгранных матчей у всех игроков
    for p in team1.players:
        p.games_played += 1
    for p in team2.players:
        p.games_played += 1

    # ---------- Формирование отчёта ----------
    full_report = f"{team1.name} {total_goals1} : {total_goals2} {team2.name} – {result_text}\n"
    full_report += "\n".join(period_reports)

    # Возвращаем подробный результат
    return {
        "score": (total_goals1, total_goals2),
        "ot_goals": (ot_goals1, ot_goals2),
        "shootout_score": (shootout_score1, shootout_score2),
        "winner": team1 if total_goals1 > total_goals2 else team2 if total_goals2 > total_goals1 else None,
        "win_type": win_type,
        "report": full_report
    }