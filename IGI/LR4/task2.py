from task2.FileManager import FileManager 
from task2.TextAnalyzer import TextAnalyzer

def main():
    """Основная функция для запуска программы анализа текста с интерактивным меню."""
    analyzer = None
    while True:
        print("\n=== Меню анализа текста ===")
        print("1. Загрузить текстовый файл")
        print("2. Подсчитать общее количество предложений")
        print("3. Подсчитать типы предложений")
        print("4. Рассчитать среднюю длину предложения")
        print("5. Рассчитать среднюю длину слова")
        print("6. Подсчитать смайлики")
        print("7. Показать слова с маленькой буквы и знаки препинания")
        print("8. Подсчитать слова, начинающиеся с согласной")
        print("9. Найти слова с двойными буквами")
        print("10. Показать слова в алфавитном порядке")
        print("11. Проверить MAC-адрес")
        print("12. Выполнить все анализы текста и сохранить результаты")
        print("13. Выход")
        choice = input("Введите ваш выбор (1-13): ").strip()
        
        if choice == "1":
            filename = input("Введите имя текстового файла: ").strip()
            text = FileManager.read_file(filename)
            if text is not None:
                analyzer = TextAnalyzer(text)
                print("Файл успешно загружен.")
            else:
                print("Не удалось загрузить файл.")
        
        elif choice == "2":
            if analyzer is None:
                print("Пожалуйста, сначала загрузите текстовый файл.")
            else:
                print(f"Всего предложений: {analyzer.count_sentences()}")
        
        elif choice == "3":
            if analyzer is None:
                print("Пожалуйста, сначала загрузите текстовый файл.")
            else:
                narrative, interrogative, imperative = analyzer.count_sentence_types()
                print(f"Повествовательные предложения: {narrative}")
                print(f"Вопросительные предложения: {interrogative}")
                print(f"Повелительные предложения: {imperative}")
        
        elif choice == "4":
            if analyzer is None:
                print("Пожалуйста, сначала загрузите текстовый файл.")
            else:
                print(f"Средняя длина предложения: {analyzer.average_sentence_length():.2f} символов")
        
        elif choice == "5":
            if analyzer is None:
                print("Пожалуйста, сначала загрузите текстовый файл.")
            else:
                print(f"Средняя длина слова: {analyzer.average_word_length():.2f} символов")
        
        elif choice == "6":
            if analyzer is None:
                print("Пожалуйста, сначала загрузите текстовый файл.")
            else:
                print(f"Количество смайликов: {analyzer.count_smileys()}")
        
        elif choice == "7":
            if analyzer is None:
                print("Пожалуйста, сначала загрузите текстовый файл.")
            else:
                lowercase_words, punctuation = analyzer.get_lowercase_words_and_punctuation()
                print(f"Слова, начинающиеся с маленькой буквы: {', '.join(lowercase_words)}")
                print(f"Знаки препинания: {', '.join(punctuation)}")
        
        elif choice == "8":
            if analyzer is None:
                print("Пожалуйста, сначала загрузите текстовый файл.")
            else:
                print(f"Слова, начинающиеся с согласной: {analyzer.count_words_starting_with_consonant()}")
        
        elif choice == "9":
            if analyzer is None:
                print("Пожалуйста, сначала загрузите текстовый файл.")
            else:
                double_letter_words = analyzer.find_words_with_double_letters()
                if double_letter_words:
                    print("Слова с двойными буквами:")
                    for pos, word in double_letter_words:
                        print(f"  Позиция {pos}: {word}")
                else:
                    print("Слов с двойными буквами не найдено.")
        
        elif choice == "10":
            if analyzer is None:
                print("Пожалуйста, сначала загрузите текстовый файл.")
            else:
                sorted_words = analyzer.get_sorted_words()
                print("Слова в алфавитном порядке:")
                print(', '.join(sorted_words))
        
        elif choice == "11":
            mac = input("Введите MAC-адрес для проверки: ").strip()
            if analyzer is None:
                analyzer_temp = TextAnalyzer("")
                if analyzer_temp.is_valid_mac_address(mac):
                    print(f"'{mac}' - действительный MAC-адрес.")
                else:
                    print(f"'{mac}' - недействительный MAC-адрес.")
            else:
                if analyzer.is_valid_mac_address(mac):
                    print(f"'{mac}' - действительный MAC-адрес.")
                else:
                    print(f"'{mac}' - недействительный MAC-адрес.")
        
        elif choice == "12":
            if analyzer is None:
                print("Пожалуйста, сначала загрузите текстовый файл.")
            else:
                results = analyzer.get_all_analyses()
                for result in results:
                    print(result)
                output_filename = "analysis_results.txt"
                FileManager.write_file(output_filename, '\n'.join(results))
                archive_name = "results.zip"
                FileManager.archive_file(output_filename, archive_name)
                archive_info = FileManager.get_archive_info(archive_name)
                if archive_info:
                    print("\nСодержимое архива:")
                    for info in archive_info:
                        print(f"  {info.filename} - {info.file_size} байт")
        
        elif choice == "13":
            print("Выход из программы.")
            break
        
        else:
            print("Неверный выбор. Пожалуйста, введите число от 1 до 13.")

if __name__ == "__main__":
    main()