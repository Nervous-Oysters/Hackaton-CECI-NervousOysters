from flask import Flask, render_template, request

app = Flask(__name__, template_folder='templates', static_folder='static')


@app.route("/")
def index():
    return render_template("stats.html")


@app.route("/player1")
def player1():
    return render_template("game.html", player_no=1)


@app.route("/cast", methods=['POST'])
def cast():
    player_id = request.form.get("player")
    spell = request.form.get("spellName")
    return "received"


@app.route("/player2")
def player2():
    return render_template("game.html", player_no=2)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
