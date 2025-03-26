# main for task4
# Task4
# Stetsurin Elisey 353504
# 23.03.2025

from text_processing import split_text, count_short_words, find_shortest_word_ending_with_w, sort_words_by_length

def run_task4():
    """
    Executes Task 4: Analyzes a predefined text for word statistics.

    This function processes a fixed text to:
    a) Count words with length less or equal than 5 characters.
    b) Find the shortest word ending with 'w'.
    c) Sort and display all words by their length.

    The function uses helper functions from text_processing.py and prints the results.
    It pauses for user input (Enter) before returning to the menu.

    Returns:
        None
    
    Notes:
        - The text analyzed is hardcoded within the function.
        - Output is formatted with separators and descriptive messages.
    """
    text = "So she was considering in her own mind, asw well as she could, for the hot day made her feel very sleepy and stupid, whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her."
    print("Анализ текста:")
    print("-" * 50)
    words = split_text(text)
    short_words_count = count_short_words(words, max_length=5)
    print(f"а) Количество слов, длина которых меньше 6 символов: {short_words_count}")
    shortest_word_with_w = find_shortest_word_ending_with_w(words)
    if shortest_word_with_w:
        print(f"б) Самое короткое слово, заканчивающееся на 'w': {shortest_word_with_w}")
    else:
        print("б) Нет слов, заканчивающихся на 'w'")
    sorted_words = sort_words_by_length(words)
    print("в) Слова в порядке возрастания их длин:")
    for word in sorted_words:
        print(f"   {word} (длина: {len(word)})")
    print("-" * 50)
    input("Нажмите Enter, чтобы вернуться в меню.")