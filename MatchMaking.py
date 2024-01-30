import json
import itertools

from pulp import LpProblem, LpVariable, lpSum, value, LpMinimize, COIN_CMD

playerDataFilePath = "PlayerData.json"
playerData = {}

# search box autocomplete for adding players
def search_player(searchTerm):
    open_data()
    a = [person["name"] for person in playerData]

    for item in playerData:
        print("list of names ", item)

    result_names = [player['name'] for player in playerData if searchTerm in player['name'].lower()]

    return result_names

#roles: 0=flex 1=first speaker etc.
def add_player(name, rating=1000, role=0):
    open_data()
    if not any(player["name"] == name for player in playerData):
        new_player = {"name": name, "rating": rating, "role": role}
        playerData.append(new_player)
    update_player_data()

def delete_player(name):
    open_data()
    open_data = [player for player in open_data if player['name'] != name.lower()]
    update_player_data()

def list_players():
    open_data()
    for name, value in playerData.items():
        if isinstance(value, dict):
            print(f"{name}:")
            for inner_key, inner_value in value.items():
                print(f"  {inner_key}: {inner_value}")
        else:
            print(f"{name}: {value}")

def open_data():
    global playerData
    with open(playerDataFilePath, 'r') as f:
        try:
            playerData = json.load(f)
        except:
            print("error with opening player data or is empty")

def update_player_data():
    with open(playerDataFilePath, 'w') as f:
        json.dump(playerData, f, indent=4)

def get_players_by_names(player_list):
    open_data()
    player_list = [player for player in playerData if player['name'] in player_list]
    return player_list

def create_teams(players : list):
    player_list = get_players_by_names(players)
    
    # team size = half of player (floor)
    team_size = len(player_list) // 2

    # Sort players by role and then by rating (ascending) note: include reverse=False for opposite 
    sorted_players = sorted(player_list, key=lambda x: (x['role'], -x['rating']), reverse=False)

    # Group players by role
    grouped_players = {"fill" : []}
    for player in sorted_players:
        role = player['role']
        if role not in grouped_players:
            grouped_players[role] = []
        grouped_players[role].append(player)

    # Initialize teams
    team1 = []
    team2 = []

    # Fill each role with one player when possible
    for role, players_list in grouped_players.items():
        if role == "fill":
            continue

        print('\n', role, players_list)

        if len(players_list) >= 2:
            if sum(player['rating'] for player in team1) <= sum(player['rating'] for player in team2):
                team1.append(players_list[0])
                team2.append(players_list[1])
            
            else:
                team2.append(players_list[0])
                team1.append(players_list[1])

            # Fill off role (3 + per role) players to second role or flex
            off_role_players = players_list[2:]

            for player in off_role_players:
                if "second_role" not in player:
                    grouped_players['fill'].append(player)
                    continue

                if player["second_role"] not in grouped_players:
                    grouped_players[role] = []
                    grouped_players[role].append(player)
                
        elif len(players_list) == 1:
            # Only one player with this role, assign to the team that needs it
            if len(team1) <= len(team2):
                team1.append(players_list[0])

            else:
                team2.append(players_list[0])

    for i, player in enumerate(grouped_players['fill']):
        if i % 2 == 0:
            team1.append(player)
        else:
            team2.append(player)

    return team1, team2

    

    # Assign last player to teams based on lower ratings
    # remaining_player = sorted_players[len(team1) + len(team2):]
    # if remaining_players:
    #     remaining_player = remaining_players[0]
    #     if sum(player['rating'] for player in team1) <= sum(player['rating'] for player in team2):
    #         print(remaining_player['name'], " TO TEAM 1 [REM]", end="\n")
    #         team1.append(remaining_player)
    #     else:
    #         print(remaining_player['name'], " TO TEAM 2 [REM]", end="\n")
    #         team2.append(remaining_player)

    return team1, team2

# def addPlayerToLower()

def main():
# Example usage
    players_list = [
        {'name': "player A", 'rating': 1100, 'role': 'speaker1'},
        {'name': "player B", 'rating': 900, 'role': 'speaker1'},
        {'name': "player C", 'rating': 1550, 'role': 'speaker1'},
        {'name': "player D", 'rating': 1250, 'role': 'speaker2'},
        {'name': "player E", 'rating': 1100, 'role': 'speaker2'},
        {'name': "player F", 'rating': 1050, 'role': 'speaker3'},
        {'name': "player G", 'rating': 1650, 'role': 'speaker3'},
        {'name': "player H", 'rating': 1650, 'role': 'speaker4'},
        {'name': "player I", 'rating': 850, 'role': 'fill'},
        {'name': "player J", 'rating': 975, 'role': 'fill'},
        {'name': "player K", 'rating': 1250, 'role': 'fill'}    
        # Add more players as needed
    ]

    team1, team2 = create_teams(players_list)
    print_teams(team1, team2)
    return

def print_teams(team1, team2):
    print("Team 1:")
    for player in team1:
        print(f"{player['name']} - {player['role']} - Rating: {player['rating']}")

    print("\nTeam 2:")
    for player in team2:
        print(f"{player['name']} - {player['role']} - Rating: {player['rating']}")
    return       

# if __name__ == "__main__":
#     main()

