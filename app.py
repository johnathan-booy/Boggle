from flask import Flask, render_template, request, session, jsonify, redirect, flash
from boggle import Boggle

BOARD_KEY = "board"
boggle_game = Boggle()
app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"


@app.route('/')
def show_homepage():
    """Show boggle game"""

    return render_template('index.html')


@app.route('/game')
def show_boggle_board():
    """Build board, store it in session and show boggle game"""

    size = request.args.get('size', boggle_game.size, type=int)

    if size > 10:
        return redirect('game?size=10')
    elif size < 5:
        return redirect('game?size=5')

    board = boggle_game.make_board(size)
    session[BOARD_KEY] = board
    return render_template('game.html', board=board)


@app.route('/validate-word')
def validate_word():
    """Check if the word is in the dictionary"""

    word = request.args["word"]
    board = session[BOARD_KEY]
    result = {'result': boggle_game.check_valid_word(board, word)}
    return result


@app.route('/post-score', methods=['POST'])
def post_score():
    """Receive score, update game_count, and adjust highscore if it was exceeded"""

    game_count = session.get('game_count', 0)
    highscore = session.get("highscore", 0)
    score = request.json["score"]

    game_count += 1
    session['game_count'] = game_count

    if highscore < score:
        session['highscore'] = score
        flash("Congratulations! You beat the highscore!")

    return "/"
