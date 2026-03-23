def ai_transfers(all_teams, user_team):
    print("\n=== TRANSFERS OF OTHER TEAMS ===")
    MIN_FORWARDS = 3
    MIN_DEFENDERS = 2
    MIN_GOALIES = 1

    teams_to_process = [t for t in all_teams if t != user_team]

    for wave in range(3):
        any_transfer = False

        for team in teams_to_process:
            forwards = [p for p in team.players if p.position == "Forward"]
            defenders = [p for p in team.players if p.position == "Defender"]
            goalies = [p for p in team.players if p.position == "Goalkeeper"]

            need_f = max(0, MIN_FORWARDS - len(forwards))
            need_d = max(0, MIN_DEFENDERS - len(defenders))
            need_g = max(0, MIN_GOALIES - len(goalies))

            if need_f > 0 or need_d > 0 or need_g > 0:
                candidates = []
                for other in all_teams:
                    if other == team:
                        continue
                    for p in other.players:
                        if p.position == "Forward":
                            if len([x for x in other.players if x.position == "Forward"]) <= MIN_FORWARDS:
                                continue
                        elif p.position == "Defender":
                            if len([x for x in other.players if x.position == "Defender"]) <= MIN_DEFENDERS:
                                continue
                        elif p.position == "Goalkeeper":
                            if len([x for x in other.players if x.position == "Goalkeeper"]) <= MIN_GOALIES:
                                continue

                        if (need_f > 0 and p.position == "Forward") or \
                           (need_d > 0 and p.position == "Defender") or \
                           (need_g > 0 and p.position == "Goalkeeper"):
                            candidates.append((other, p))

                candidates.sort(key=lambda x: x[1].skill, reverse=True)

                for other, p in candidates:
                    if team.budget >= p.price:
                        team.budget -= p.price
                        other.budget += p.price
                        other.players.remove(p)
                        team.players.append(p)
                        print(f"{team.name} bought {p.name} from {other.name} for {p.price} million rubles")
                        any_transfer = True
                        if p.position == "Forward":
                            need_f -= 1
                        elif p.position == "Defender":
                            need_d -= 1
                        else:
                            need_g -= 1
                        if need_f <= 0 and need_d <= 0 and need_g <= 0:
                            break

        for team in teams_to_process:
            forwards = [p for p in team.players if p.position == "Forward"]
            defenders = [p for p in team.players if p.position == "Defender"]
            goalies = [p for p in team.players if p.position == "Goalkeeper"]

            need_f = max(0, MIN_FORWARDS - len(forwards))
            need_d = max(0, MIN_DEFENDERS - len(defenders))
            need_g = max(0, MIN_GOALIES - len(goalies))

            if need_f == 0 and need_d == 0 and need_g == 0:
                continue

            surplus_players = []
            if len(forwards) > MIN_FORWARDS:
                surplus_players.extend(forwards)
            if len(defenders) > MIN_DEFENDERS:
                surplus_players.extend(defenders)
            if len(goalies) > MIN_GOALIES:
                surplus_players.extend(goalies)

            if not surplus_players:
                continue

            surplus_players.sort(key=lambda x: x.skill)
            
            for sale_candidate in surplus_players[:1]:
                for buyer in all_teams:
                    if buyer == team:
                        continue
                    if sale_candidate.position == "Forward":
                        if len([p for p in buyer.players if p.position == "Forward"]) <= MIN_FORWARDS:
                            continue
                    elif sale_candidate.position == "Defender":
                        if len([p for p in buyer.players if p.position == "Defender"]) <= MIN_DEFENDERS:
                            continue
                    else:
                        if len([p for p in buyer.players if p.position == "Goalkeeper"]) <= MIN_GOALIES:
                            continue
                    if buyer.budget >= sale_candidate.price:
                        team.budget += sale_candidate.price
                        buyer.budget -= sale_candidate.price
                        team.players.remove(sale_candidate)
                        buyer.players.append(sale_candidate)
                        print(f"{team.name} sold {sale_candidate.name} teams {buyer.name} for {sale_candidate.price} million rubles")
                        any_transfer = True
                        break
            
        for team in teams_to_process:
            forwards = [p for p in team.players if p.position == "Forward"]
            defenders = [p for p in team.players if p.position == "Defender"]
            goalies = [p for p in team.players if p.position == "Goalkeeper"]

            need_f = max(0, MIN_FORWARDS - len(forwards))
            need_d = max(0, MIN_DEFENDERS - len(defenders))
            need_g = max(0, MIN_GOALIES - len(goalies))

            if need_f > 0 or need_d > 0 or need_g > 0:
                continue 

            for pos in ["Forward", "Defender", "Goalkeeper"]:
                current_players = [p for p in team.players if p.position == pos]
                if not current_players:
                    continue
                avg_skill = sum(p.skill for p in current_players) / len(current_players)
                candidates = []
                for other in all_teams:
                    if other == team:
                        continue
                    for p in other.players:
                        if p.position == pos and p.skill > avg_skill:
                            if pos == "Forward":
                                if len([x for x in other.players if x.position == "Forward"]) <= MIN_FORWARDS:
                                    continue
                            elif pos == "Defender":
                                if len([x for x in other.players if x.position == "Defender"]) <= MIN_DEFENDERS:
                                    continue
                            else:
                                if len([x for x in other.players if x.position == "Goalkeeper"]) <= MIN_GOALIES:
                                    continue
                            candidates.append((other, p))
                if not candidates:
                    continue
                candidates.sort(key=lambda x: x[1].skill, reverse=True)
                for other, candidate in candidates:
                    if team.budget >= candidate.price:
                        worst = min(current_players, key=lambda x: x.skill)
                        if candidate.skill > worst.skill:
                            if pos == "Forward":
                                if len(current_players) <= MIN_FORWARDS:
                                    continue
                            elif pos == "Defender":
                                if len(current_players) <= MIN_DEFENDERS:
                                    continue
                            else:
                                if len(current_players) <= MIN_GOALIES:
                                    continue
                            team.budget -= candidate.price
                            other.budget += candidate.price
                            other.players.remove(candidate)
                            team.players.remove(worst)
                            team.players.append(candidate)
                            other.players.append(worst)
                            print(f"{team.name} bought {candidate.name} from {other.name} "
                                  f"For {candidate.price} million, sold {worst.name}")
                            any_transfer = True
                            break

        if not any_transfer:
            break
    print("Transfers of other team ended")
