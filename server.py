import os
import requests
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta

CACHE_DIR = './cache'
wordle_dictionary = set()
word_frequencies = {}
first_word_frequencies = {}

with open("./wordle-dictionary.txt", "r") as f:
  total_words = sum(1 for _ in f)

with open("./wordle-dictionary.txt", "r") as f:
  for idx, line in enumerate(f):
    word = line.strip()
    normalized_frequency = 1 - (idx / total_words)
    word_frequencies[word] = normalized_frequency

with open("./wordle-dictionary-first-word-frequency.txt", "r") as f:
  total_words = sum(1 for _ in f)

with open("./wordle-dictionary-first-word-frequency.txt", "r") as f:
  for idx, line in enumerate(f):
    word = line.strip()
    normalized_frequency = 1 - (idx / total_words)
    first_word_frequencies[word] = normalized_frequency

with open("./wordle-dictionary.txt", "r") as f:
    for line in f:
        wordle_dictionary.add(line.strip())

def process_user_input(user_input):
    lines = user_input.strip().split("\n")
    
    # Extract Wordle number
    wordle_num = int(lines[0].split()[1])
    print(wordle_num)
    
    start_date = datetime(2023, 10, 2)
    target_date = start_date + timedelta(days=wordle_num - 835)
    
    # Convert the squares to fit existing format
    square_translations = {
        "⬛": "⬛",
        "🟩": "🟩",
        "🟨": "🟨",
        "🟧": "🟧",
        "🟥": "🟥"
    }
    squares = [list(map(square_translations.get, list(line))) for line in lines[1:]]
    
    return target_date, squares

def fetch_wordle_solution(date):
  cache_file_path = os.path.join(CACHE_DIR, f"{date.strftime('%Y-%m-%d')}.json")

  if os.path.exists(cache_file_path):
    with open(cache_file_path, 'r') as f:
      data = json.load(f)
  else:
    url = f"https://www.nytimes.com/svc/wordle/v2/{date.strftime('%Y-%m-%d')}.json"
    response = requests.get(url)
    data = response.json()
    with open(cache_file_path, 'w') as f:
      f.write(response.text)

  return data["solution"]

def difference_from_correct(word, correct_word):
    # count how many letters are different between the word and the correct_word
    return sum(1 for w, c in zip(word, correct_word) if w != c)

# weight of weights
MAX_GENERAL_BONUS = .01
MAX_FIRST_WORD_BONUS = 5

def score_word(word, guess, correct_word):
  score = 0
  GREEN_SCORE = 3  
  YELLOW_SCORE = 1  
  BLACK_SCORE = -3  
  
  for idx, g in enumerate(guess):
      letter = word[idx]
      if g == "🟩" and letter == correct_word[idx]:
          score += GREEN_SCORE
      elif g == "🟨" and letter in correct_word and letter != correct_word[idx]:
          score += YELLOW_SCORE
      elif g == "⬛" and letter in correct_word:
          score += BLACK_SCORE
  
  # deduct points from words that are too similar to the correct word
  min_difference_required = 5 - sum(tile == "🟩" for tile in guess)  # 5 - number of green tiles
  actual_difference = difference_from_correct(word, correct_word)
  if actual_difference < min_difference_required:
      score -= (min_difference_required - actual_difference) * 10
  
  # add general frequency bonus
  if word in word_frequencies:
      score += word_frequencies[word] * MAX_GENERAL_BONUS

  # add first word frequency bonus
  if word in first_word_frequencies:
      score += first_word_frequencies[word] * MAX_FIRST_WORD_BONUS

  return score


def probable_first_guesses_with_all_guesses(correct_word, all_guesses):
    word_scores = {word: 0 for word in wordle_dictionary}
    
    for guess in all_guesses:
        for word in wordle_dictionary:
            word_scores[word] += score_word(word, guess, correct_word)

    sorted_word_scores = sorted(word_scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_word_scores  # Return the list of tuples, not just the words


app = Flask(__name__)
CORS(app)

@app.route('/predict', methods=['POST'])
def predict():
  # process request as string
  user_input = request.get_data(as_text=True)
  
  if not user_input:
    return jsonify({'error': 'User input is missing or empty'}), 400

  target_date, all_guesses_test = process_user_input(user_input)
  correct_word = fetch_wordle_solution(target_date)

  top_probable_first_guesses = probable_first_guesses_with_all_guesses(correct_word, all_guesses_test)

  response = jsonify({
    # 'correct_word': correct_word,
    'target_date': target_date.strftime('%Y-%m-%d'),
    'top_probable_first_guesses': top_probable_first_guesses[:10]
  })
  
  response.headers.add('Access-Control-Allow-Origin', '*')

  return response

if __name__ == "__main__":
    app.run(debug=True)