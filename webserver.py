from flask import Flask, render_template, request


app = Flask(__name__, template_folder='templates', static_folder='static')
spell = 'nothing'
cast.has_been_called = False
player_id = 0
not_player = 0

@app.route("/")
def index():
    return render_template("stats.html")


@app.route("/player1")
def player1():
    return render_template("game.html", player_no=1)


@app.route("/cast", methods=['POST'])
def cast():
    player_id = request.form.get("player")
    if player_id == 1:
        not_player = 2
    else:
        not_player = 1
    spell = request.form.get("spellName")
    cast.has_been_called = True
    return "received"


@app.route("/player2")
def player2():
    return render_template("game.html", player_no=2)




if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)




