from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle
from app import BOARD_KEY


class FlaskTests(TestCase):

    def setUp(self):
        """Executed before every test"""
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_show_boggle_board(self):
        """Make sure information is in the session and the HTML is displayed"""

        with self.client:
            response = self.client.get('/game')
            self.assertIn(BOARD_KEY, session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('game-count'))
            self.assertIn(b'<div id="timer" class="statistic">', response.data)
            self.assertIn(b'<div id="score" class="statistic">', response.data)
            self.assertIn(
                b'<div id="highscore" class="statistic">', response.data)
            self.assertIn(
                b'<div id="game-counter" class="statistic">', response.data)

    def setup_validate_word(self):
        with self.client as client:
            with client.session_transaction() as change_session:
                change_session[BOARD_KEY] = [['R', 'C', 'N', 'L', 'Q'],
                                             ['T', 'E', 'W', 'C', 'I'],
                                             ['D', 'I', 'T', 'T', 'U'],
                                             ['I', 'N', 'A', 'T', 'L'],
                                             ['N', 'L', 'Y', 'O', 'O']]

    def test_valid_word(self):
        """Test if a word in the board will be validated"""
        self.setup_validate_word()

        response = self.client.get('/validate-word?word=otter')
        self.assertEqual(response.json['result'], 'ok')

    def test_invalid_word(self):
        """Test if a valid word that is not on the board will be rejected"""
        self.setup_validate_word()

        response = self.client.get('/validate-word?word=brother')
        self.assertEqual(response.json['result'], 'not-on-board')

    def test_not_word(self):
        """Test if an invalid word will be rejected"""
        self.setup_validate_word()

        response = self.client.get('/validate-word?word=wiebfiasndflknkl')
        self.assertEqual(response.json['result'], 'not-word')
