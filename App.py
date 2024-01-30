from flask import *
import MatchMaking

app=Flask(__name__)

@app.route("/")
def upload():
    return render_template("match_making.html")

@app.route("/start_match")
def upload_matchmaking():
    return render_template("create_match.html")
    
@app.route("/search", methods=["GET"])
def search_name():
    search_term = request.args.get('search_term', '').lower()
    print("searched term", search_term)
    result_names = MatchMaking.search_player(search_term)
    print("found names", result_names)
    return jsonify(result_names)

@app.route("/create_teams", methods=["GET"])
def create_team():
    player_list_json = request.args.get('added_players')
    player_list = json.loads(player_list_json)   
    
    team1, team2 = MatchMaking.create_teams(player_list)
    return jsonify(team1, team2)


if __name__ == "__main__":
    app.run(debug = True)

