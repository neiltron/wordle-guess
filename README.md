# wordle-guess

A little experiment to predict first-word guesses in Wordle based on the Share output. It parses the Wordle number from the share text, fetches the answer for that day, and builds word scores from there.

This process is based on probability working backwards from the answer. A score is derived based on:
- The color of blocks in each guess, eliminating or down-ranking certain words that are more or less likely.
- The frequency of use in English (based on a [Wortschatz](https://wortschatz.uni-leipzig.de/en/download/English) dataset)
- Frequency of use in Wordle [starting guesses](https://www.nytimes.com/interactive/2022/upshot/wordle-bot.html).