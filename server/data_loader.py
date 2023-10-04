wordle_dictionary = set()
word_frequencies = {}
first_word_frequencies = {}

def load_wordle_dictionary():
    global wordle_dictionary
    with open("./data/wordle-dictionary.txt", "r") as f:
        for line in f:
            wordle_dictionary.add(line.strip())

def load_word_frequencies():
    global word_frequencies
    with open("./data/wordle-dictionary.txt", "r") as f:
        total_words = sum(1 for _ in f)
        
    with open("./data/wordle-dictionary.txt", "r") as f:
        for index, line in enumerate(f):
            word = line.strip()
            normalized_frequency = 1 - (index / total_words)
            word_frequencies[word] = normalized_frequency

def load_first_word_frequencies():
    global first_word_frequencies
    with open("./data/wordle-dictionary-first-word-frequency.txt", "r") as f:
        total_words = sum(1 for _ in f)

    with open("./data/wordle-dictionary-first-word-frequency.txt", "r") as f:
        for index, line in enumerate(f):
            word = line.strip()
            normalized_frequency = 1 - (index / total_words)
            first_word_frequencies[word] = normalized_frequency

def initialize_data():
    load_wordle_dictionary()
    load_word_frequencies()
    load_first_word_frequencies()
