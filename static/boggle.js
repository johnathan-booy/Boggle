class BoggleGame {
	constructor(boardId) {
		this.$timer = $("#timer");
		this.$scoreText = $("#score .statistic-content span");
		this.$highscoreText = $("#highscore .statistic-content span");
		this.$timerText = $("#timer .statistic-content span");
		this.$guessForm = $("#guess-form");
		this.$board = $("#board");
		this.$notify = $("#notify");

		this.score = 0;
		this.guessedWords = new Set();
		this.timer = 10;

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
			this.$notify.addClass("notify-bad");
			this.$notify.html(`You've already guessed '${wordCased}'!`);
		} else if (word.length < 2) {
			this.$notify.addClass("notify-bad");
			this.$notify.html(`Words must be at least two characters long!`);
		} else if (validation.result === "not-on-board") {
			this.$notify.addClass("notify-bad");
			this.$notify.html(`'<span>${wordCased}</span>' is not on the board!`);
		} else if (validation.result === "not-word") {
			this.$notify.addClass("notify-bad");
			this.$notify.html(`'<span>${wordCased}</span>' is not a word!`);
		} else if (validation.result === "ok") {
			this.$notify.addClass("notify-good");
			this.$notify.html(`You found the word '<span>${wordCased}</span>'!`);
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
	}

	removeBoard() {
		this.$timer.remove();
		this.$guessForm.remove();
		this.$board.remove();
	}

	async processResult() {
		const res = await axios.post("/post-score", { score: this.score });
		console.log(res.data);
		this.displayResult(res.data);
	}

	displayResult(results) {
		this.updateHighscore(results["highscore"]);
		this.$notify.removeClass();
		this.$notify.addClass("notify-good");
		this.$notify.html(`<b>Game Over!</b>`);
	}
}
