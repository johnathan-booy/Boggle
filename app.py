from flask import Flask, render_template, request, session
from boggle import Boggle

BOARD_KEY = "board"
boggle_game = Boggle(size=6)
app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"


@app.route('/')
def show_boggle_board():
    board = boggle_game.make_board()
    session[BOARD_KEY] = board
    return render_template('index.html', board=board)


@app.route('/validate-word')
def validate_word():
    word = request.args["word"]
    board = session[BOARD_KEY]
    result = {'result': boggle_game.check_valid_word(board, word)}
    return result
