from flask import Flask, render_template, request
import main
import spell

app = Flask(__name__, template_folder='templates', static_folder='static')


@app.route("/")
def index():
    return render_template("stats.html")


@app.route("/player1")
def player1():
    return render_template("game.html", player_no=1)


spell_corresp = {
    "fire": "fire-ball_10" ,
    "ultimate": "send-oyster_10",
    "water": "send-waterenergy_10",
    "energy": "send-waterenergy_10",
}

@app.route("/cast", methods=['POST'])
def cast():
    player_id = request.form.get("player")
    spell_name = request.form.get("spellName")
    # main.pre_process_spells.append(("fire-ball_10", 5,player_id))
    with open("spells.csv","w") as file:
        file.write(f"{spell_corresp[spell_name]},5,{player_id},{spell_name}")
    return "success!"


@app.route("/player2")
def player2():
    return render_template("game.html", player_no=2)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
