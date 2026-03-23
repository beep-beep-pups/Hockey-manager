import random
from ai_transfers import ai_transfers
def transfer_market(user_team, all_teams, playoffs_in_progress):
    if playoffs_in_progress:
        print("Playoff not ended")
        return
    
    while True:
        print("\n--- Transfers ---")
        print(f"Your budget: {user_team.budget} million rubles")
        print("1 Buy player")
        print("2 Sell player")
        print("3 Complete transfers")
        print("4 Exit")

        choice = input("Ыelect an action: ").strip()
        if choice == "1":
            buy_player(user_team, all_teams)
        elif choice == "2":
            sell_player(user_team, all_teams)
        elif choice == "3":
            ai_transfers(all_teams, user_team)
            break
        else:
            break
def buy_player(user_team, all_teams):
    available = []
    for team in user_team:
        if team != user_team:
            for p in team.players:
                available.append((team, p))
    if not available:
        print("There are no available players")
        return
    print("\nAvailable players:")
    for i, (team, p) in enumerate(available, 1):
        print(f"{i}. {p.name} ({p.position}): skill - {p.skill}, price - {p.price} million rubles, team - {team.name}")
    try: 
        idx = int(input("Player number for purchase (0 for cancellation): ")) - 1
        if idx < 0 or idx >= len(available):
            return
        team ,player = available[idx]

        if player.position == "Forward":
            pos_count = len([p for p in team.players if p.position == "Forward"])
            if pos_count <= 3:
                print(f"You cannot buy {player.name}: the team {team.name} will have fewer than 3 forwards")
                return
        elif player.position == "Defender":
            pos_count = len([p for p in team.players if p.position == "Defender"])
            if pos_count <= 2:
                print(f"You cannot buy {player.name}: the team {team.name} will have fewer than 2 defenders")
                return
        else:
            pos_count = len([p for p in team.players if p.position == "Goalkeeper"])
            if pos_count <= 1:
                print(f"You cannot buy {player.name}: the team {team.name} will have fewer than 1 goalkeeper")
                return
            
        if user_team.budget >= player.price:
            user_team.budget -= player.price
            team.budget += player.price
            team.players.remove(player)
            user_team.players.append(player)
            print(f"You bought {player.name} for {player.price} million rubles. New budget: {user_team.budget} million rubles")
        else:
            print("Money not enough")
    except ValueError:
        print("Incorrect input")

def sell_player(user_team, all_teams):
    if not user_team.players:
        print("There are no players in your team")
        return
    print("\nYour players:")
    for i, p in enumerate(user_team.players, 1):
        print(f"{i}. {p.name} ({p.position}): skill - {p.skill}, price - {p.price} million rubles")
    try:
        idx = int(input("Player number for sell (0 for cancellation): ")) - 1
        if idx < 0 or idx >= len(user_team.players):
            return
        player = user_team.players[idx]

        if player.position == "Forward":
            pos_count = len([p for p in user_team.players if p.position == "Forward"])
            if pos_count <= 3:
                print(f"You cannot buy {player.name}: your team will have fewer than 3 forwards")
                return
        elif player.position == "Defender":
            pos_count = len([p for p in user_team.players if p.position == "Defender"])
            if pos_count <= 2:
                print(f"You cannot buy {player.name}: your team will have fewer than 2 defenders")
                return
        else:
            pos_count = len([p for p in user_team.players if p.position == "Goalkeeper"])
            if pos_count <= 1:
                print(f"You cannot buy {player.name}: your team will have fewer than 1 goalkeeper")
                return
        user_team.budget += player.price
        user_team.players.remove(player)
        for team in [t for t in all_teams if t != user_team and t.budget >= player.price]:
            team.players.append(player)
            team.budget -= player.price
            break
        print(f"You sold {player.name} for {player.price} million. New budget: {user_team.budget} million rubles")
    except ValueError:
        print("Incorect input") 
