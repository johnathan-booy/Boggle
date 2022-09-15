class BoggleGame {
	constructor(boardId) {
		$("#guess-form").on("submit", this.handleSubmit.bind(this));
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
		const $notify = $("#notify");
		const wordCased = word.toUpperCase();

		$notify.removeClass();

		if (validation.result === "ok") {
			$notify.addClass("notify-good");
			$notify.html(`You found the word '<span>${wordCased}</span>'!`);
		} else if (validation.result === "not-on-board") {
			$notify.addClass("notify-bad");
			$notify.html(`'<span>${wordCased}</span>' is not on the board!`);
		} else if (validation.result === "not-word") {
			$notify.addClass("notify-bad");
			$notify.html(`'<span>${wordCased}</span>' is not a word!`);
		} else {
			$notify.addClass("hidden");
		}
	}
}
