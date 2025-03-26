# logic for task3 & task4
# Stetsurin Elisey 353504
# 23.03.2025

from decorator import log_decorator

@log_decorator
def count_whitespace_and_apostrophes(text):
    """
    Counts the number of whitespace characters and apostrophes in the text.

    Args:
        text (str): The input text to analyze.

    Returns:
        tuple: A tuple (whitespace_count, apostrophe_count) where:
            - whitespace_count (int): Number of whitespace characters.
            - apostrophe_count (int): Number of apostrophes (').
    """
    whitespace_count = 0
    apostrophe_count = 0
    
    for char in text:
        if char.isspace():  # check if space
            whitespace_count += 1
        elif char == "'":  # check if '
            apostrophe_count += 1
    
    return whitespace_count, apostrophe_count

@log_decorator
def split_text(text):
    """
    Splits the text into words based on spaces and commas.

    This function replaces all commas in the text with spaces and then splits the resulting string
    into a list of words using spaces as delimiters.

    Args:
        text (str): The input text to be split.

    Returns:
        list: A list of words extracted from the text.
    """
    return text.replace(',', ' ').split()

@log_decorator
def count_short_words(words, max_length=5):
    """
    Counts the number of words with length less than or equal to max_length.

    Args:
        words (list): A list of words to analyze.
        max_length (int, optional): The maximum length of words to count. Defaults to 5.

    Returns:
        int: The number of words in the list with length less than or equal to max_length.
    """
    return sum(1 for word in words if len(word) <= max_length)

@log_decorator
def find_shortest_word_ending_with_w(words):
    """
    Finds the shortest word that ends with 'w' (case insensitive).

    This function filters the list for words ending with 'w' (ignoring case) and returns the shortest one.
    If no such word exists, it returns None.

    Args:
        words (list): A list of words to search through.

    Returns:
        str or None: The shortest word ending with 'w', or None if no such word is found.
    """
    ending_with_w = [word for word in words if word.lower().endswith('w')]
    if not ending_with_w:
        return None
    return min(ending_with_w, key=len)

@log_decorator
def sort_words_by_length(words):
    """
    Sorts the words by their length in ascending order.

    Args:
        words (list): A list of words to sort.

    Returns:
        list: A new list containing the words sorted by their length.
    """
    return sorted(words, key=len)