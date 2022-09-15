from flask import Flask, render_template
from boggle import Boggle

boggle_game = Boggle()

app = Flask(__name__)


@app.route('/')
def show_boggle_board():
    board = boggle_game.make_board()
    return render_template('boggle.html', board=board)
