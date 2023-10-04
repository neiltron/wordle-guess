from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta

from data_loader import initialize_data
from scoring import probable_first_guesses_with_all_guesses
from nyt_fetch import fetch_wordle_solution


def process_user_input(user_input):
  lines = user_input.strip().split("\n")
  
  # extract Wordle number
  try:
    wordle_num = int(lines[0].split()[1])
  except (IndexError, ValueError):
    raise ValueError('Invalid Wordle number')
  
  print(wordle_num)
  
  start_date = datetime(2023, 10, 2)
  target_date = start_date + timedelta(days=wordle_num - 835)
  
  squares = [list(line) for line in lines[1:]]
  
  return target_date, squares

initialize_data()
app = Flask(__name__)
CORS(app)

@app.route('/predict', methods=['POST'])
def predict():
  # process request as string
  user_input = request.get_data(as_text=True)
  
  if not user_input:
    return jsonify({'error': 'User input is missing or empty'}), 400

  try:
    target_date, all_guesses_test = process_user_input(user_input)
    correct_word = fetch_wordle_solution(target_date)
  except ValueError as e:
    return jsonify({'error': str(e)}), 400

  top_probable_first_guesses = probable_first_guesses_with_all_guesses(correct_word, all_guesses_test)

  response = jsonify({
    # 'correct_word': correct_word,
    'target_date': target_date.strftime('%Y-%m-%d'),
    'top_probable_first_guesses': top_probable_first_guesses[:50]
  })
  
  response.headers.add('Access-Control-Allow-Origin', '*')

  return response

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5001)