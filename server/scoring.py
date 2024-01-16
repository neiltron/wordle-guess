from data_loader import wordle_dictionary, word_frequencies, first_word_frequencies
from Levenshtein import distance

MAX_GENERAL_BONUS = .001
MAX_FIRST_WORD_BONUS = 1
ELIMINATE_SCORE = -1e9

def difference_from_correct(word, correct_word):
    return distance(word, correct_word)

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
    # if actual_difference < min_difference_required:
    #     scaling_factor = (num_guesses / 6) ** 0.8
    #     score -= (min_difference_required - actual_difference) * 10 * scaling_factor
  
    if word in word_frequencies:
        score += word_frequencies[word] * MAX_GENERAL_BONUS

    if word in first_word_frequencies:
        score += first_word_frequencies[word] * MAX_FIRST_WORD_BONUS

    return score

def modified_score_word(word, guess, correct_word, num_guesses):
    score = 0
    GREEN_SCORE = 3  
    YELLOW_SCORE = 1  
    BLACK_SCORE = -3  
    ELIMINATE_SCORE = -1e9  # Large negative value to essentially "eliminate" the word
    
    # 1. Green Blocks logic
    for idx, g in enumerate(guess):
        letter = word[idx]
        if g == "🟩" and letter != correct_word[idx]:
            return ELIMINATE_SCORE  # Eliminate word if it doesn't match green block
    
    # 2. Yellow Blocks logic
    yellow_count = sum(tile == "🟨" for tile in guess)
    common_letters = set(word).intersection(set(correct_word))
    if len(common_letters) < yellow_count:
        return ELIMINATE_SCORE  # Eliminate word if it doesn't have enough common letters

    return score


def probable_first_guesses_with_all_guesses(correct_word, all_guesses):
    word_scores = {word: 0 for word in wordle_dictionary}
    
    for guess in all_guesses:
        for word in wordle_dictionary:
            word_scores[word] += score_word(word, guess, correct_word, len(all_guesses))

    sorted_word_scores = sorted(word_scores.items(), key=lambda x: x[1], reverse=True)
    sorted_word_scores = second_pass_filtering(sorted_word_scores, all_guesses[0], correct_word)

    return sorted_word_scores

def second_pass_filtering(predictions, first_guess, correct_word):
    # Iterate over the predictions and set the score to 0 for words that don't meet the criteria
    filtered_predictions = []
    for word, score in predictions:
        if modified_score_word(word, first_guess, correct_word, 1) != ELIMINATE_SCORE:
            filtered_predictions.append((word, score))

    print(filtered_predictions)
    
    return filtered_predictions


def enhanced_probable_first_guesses(correct_word, all_guesses):
    # Initial scoring using the original function
    initial_predictions = probable_first_guesses_with_all_guesses(correct_word, all_guesses)
    
    # Filter the initial predictions using the modified_score_word function
    # filtered_predictions = second_pass_filtering(initial_predictions, all_guesses[0], correct_word)
    
    return initial_predictions