class BoggleGame {
	constructor(boardId) {
		this.$newGame = $("#new-game");
		this.$timer = $("#timer");
		this.$scoreText = $("#score .statistic-content span");
		this.$highscoreText = $("#highscore .statistic-content span");
		this.$timerText = $("#timer .statistic-content span");
		this.$guessForm = $("#guess-form");
		this.$board = $("#board");
		this.$notify = $("#notify");

		this.score = 0;
		this.guessedWords = new Set();
		this.timer = 8;

		this.timerInterval = setInterval(this.updateTimer.bind(this), 1000);
		this.$guessForm.on("submit", this.handleSubmit.bind(this));
	}

	async handleSubmit(e) {
		e.preventDefault();

		const $guessInput = $("#guess-input");
		const word = $guessInput.val();
		$guessInput.val("");

		const validation = await this.validateWord(word);
		this.displayValidation(validation, word);
	}

	async validateWord(word) {
		const res = await axios.get("/validate-word", { params: { word: word } });
		return res.data;
	}

	displayValidation(validation, word) {
		const wordCased = word.toUpperCase();

		this.$notify.removeClass();
		if (this.guessedWords.has(wordCased)) {
			this.showMessage(`You've already guessed '${wordCased}'!`, "notify-bad");
		} else if (word.length < 2) {
			this.showMessage(
				`Words must be at least two characters long!`,
				"notify-bad"
			);
		} else if (validation.result === "not-on-board") {
			this.showMessage(
				`'<span>${wordCased}</span>' is not on the board!`,
				"notify-bad"
			);
		} else if (validation.result === "not-word") {
			this.showMessage(
				`'<span>${wordCased}</span>' is not a word!`,
				"notify-bad"
			);
		} else if (validation.result === "ok") {
			this.showMessage(
				`You found the word '<span>${wordCased}</span>'!`,
				"notify-good"
			);
			this.updateScore(word.length);
			this.guessedWords.add(wordCased);
		}
	}

	updateScore(num) {
		this.score = this.score + num;
		this.$scoreText.text(this.score);
	}

	updateHighscore(num) {
		this.$highscoreText.text(num);
	}

	updateTimer() {
		this.timer--;
		if (this.timer <= 0) {
			this.gameOver();
		}
		this.$timerText.text(this.timer);
	}

	gameOver() {
		clearInterval(this.timerInterval);
		this.removeBoard();
		this.processResult();
		this.$newGame.removeClass("hidden");
	}

	removeBoard() {
		this.$timer.remove();
		this.$guessForm.remove();
		this.$board.remove();
	}

	async processResult() {
		const res = await axios.post("/post-score", { score: this.score });
		this.displayResult(res.data);
	}

	displayResult(results) {
		const { score, highscore, brokeRecord } = results;

		console.log(highscore);
		this.updateHighscore(highscore);

		if (brokeRecord) {
			this.showMessage(
				"Congratulations, you got a new highscore!",
				"notify-good"
			);
		} else {
			this.showMessage("Nice Work!", "notify-good");
		}
	}

	showMessage(html, cls) {
		this.$notify.removeClass();
		this.$notify.addClass(cls);
		this.$notify.html(html);
	}
}
