from data_loader import wordle_dictionary, word_frequencies, first_word_frequencies

MAX_GENERAL_BONUS = .001
MAX_FIRST_WORD_BONUS = 1

def difference_from_correct(word, correct_word):
    return sum(1 for w, c in zip(word, correct_word) if w != c)

def score_word(word, guess, correct_word, num_guesses):
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
  
    min_difference_required = 5 - sum(tile == "🟩" for tile in guess)
    actual_difference = difference_from_correct(word, correct_word)
    if actual_difference < min_difference_required:
        scaling_factor = (num_guesses / 6) ** 0.8
        score -= (min_difference_required - actual_difference) * 10 * scaling_factor
  
    if word in word_frequencies:
        score += word_frequencies[word] * MAX_GENERAL_BONUS

    if word in first_word_frequencies:
        score += first_word_frequencies[word] * MAX_FIRST_WORD_BONUS

    return score

def probable_first_guesses_with_all_guesses(correct_word, all_guesses):
    word_scores = {word: 0 for word in wordle_dictionary}
    
    for guess in all_guesses:
        for word in wordle_dictionary:
            word_scores[word] += score_word(word, guess, correct_word, len(all_guesses))

    sorted_word_scores = sorted(word_scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_word_scores
