# main for task4
# Task4
# Stetsurin Elisey 353504
# 23.03.2025

from text_processing import split_text, count_short_words, find_shortest_word_ending_with_w, sort_words_by_length

text = "So she was considering in her own mind, asw well as she could, for the hot day made her feel very sleepy and stupid, whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her."
    
print("Анализ текста:")
print("-" * 50)
    
words = split_text(text)
    
# а) Подсчёт слов, длина которых меньше 6 символов
short_words_count = count_short_words(words, max_length=5)
print(f"а) Количество слов, длина которых меньше 6 символов: {short_words_count}")
    
# б) Поиск самого короткого слова, заканчивающегося на 'w'
shortest_word_with_w = find_shortest_word_ending_with_w(words)
if shortest_word_with_w:
    print(f"б) Самое короткое слово, заканчивающееся на 'w': {shortest_word_with_w}")
else:
    print("б) Нет слов, заканчивающихся на 'w'")
    
# в) Вывод всех слов в порядке возрастания их длин
sorted_words = sort_words_by_length(words)
print("в) Слова в порядке возрастания их длин:")
for word in sorted_words:
    print(f"   {word} (длина: {len(word)})")