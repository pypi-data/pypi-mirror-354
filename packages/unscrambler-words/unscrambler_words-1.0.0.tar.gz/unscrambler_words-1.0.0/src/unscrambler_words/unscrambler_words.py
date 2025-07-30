import pandas as pd
import itertools

# Reads a text file where each line is a word and returns a DataFrame.
def create_dataframe_from_txt(file_path):
    df = pd.read_csv(file_path, header=None, names=['word'])
    return df

# Converts the 'word' column of a DataFrame into a set for fast lookup.
def load_word_list_from_dataframe(df):
    return set(df['word'].str.lower())

# Returns all valid words that can be formed from the scrambled word.
def unscramble(scrambled_word, word_list):
    permutations = set(''.join(p) for p in itertools.permutations(scrambled_word.lower()))
    valid_words = permutations.intersection(word_list)
    return valid_words

# Replace this with the actual path to your word list file
file_path = input("Enter file path for word list \n").strip('"')

# Load the word list into a DataFrame
df = create_dataframe_from_txt(file_path)

# Convert the DataFrame to a set of words
word_list = load_word_list_from_dataframe(df)

# Prompt the user for input
scrambled_word = input("Enter a scrambled word: ").replace(" ", "")

# Find and print all valid words
valid_words = unscramble(scrambled_word, word_list)

if valid_words:
    print(f"Valid words for '{scrambled_word}': {valid_words}")

else:
    print(f"No valid English words found for '{scrambled_word}'.")

