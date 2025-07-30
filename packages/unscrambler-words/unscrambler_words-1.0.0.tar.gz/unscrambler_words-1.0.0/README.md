**Overview**

**Word Unscrambler** is a Python script that finds valid words from scrambled letters using permutations. It relies on **pandas** for word list management and **itertools** for generating word permutations.

**Installation**

Ensure Python (>=3.7) is installed and install the necessary dependency:

pip install pandas

**Usage**

Run the script and provide:

1. A text file (words.txt) with a list of words (one per line).
2. A scrambled word to unscramble.

**Functions**

_create_dataframe_from_txt(file_path)_

**Reads a text file and converts it into a pandas DataFrame.**

- **Parameter:** file_path _(str)_ – Path to the word list file.
- **Returns:** DataFrame – Contains words from the file.

_load_word_list_from_dataframe(df)_

**Converts the word column in the DataFrame into a lowercase set for quick lookup.**

- **Parameter:** df _(DataFrame)_ – Word list DataFrame.
- **Returns:** set – Unique words for easy searching.

_unscramble(scrambled_word, word_list)_

**Generates all possible permutations of the scrambled word and checks against the word list.**

- **Parameters:**
  - scrambled_word _(str)_ – The input scrambled word.
  - word_list _(set)_ – Set of valid words.
- **Returns:** set – Valid words matching permutations.

**Execution Flow**

1. Prompt the user for the word list file path.
2. Load words into a pandas DataFrame.
3. Convert DataFrame into a lookup set.
4. Prompt the user for scrambled input.
5. Generate word permutations.
6. Compare against the word list and return valid words.

**Example Usage**

1. python unscrambler.py
2. Enter file path for word list:  
    words.txt
3. Enter a scrambled word:  
    tap

**Expected Output**

Valid words for 'tap': {'tap', 'pat', 'apt'}

**License**

This project is licensed under The Unlicense