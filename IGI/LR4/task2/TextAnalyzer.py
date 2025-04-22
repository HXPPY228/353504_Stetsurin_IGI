import re

class TextAnalyzer:
    """Class for analyzing text and extracting various statistics."""
    
    def __init__(self, text):
        """
        Initialize the TextAnalyzer with the given text.
        
        Args:
            text (str): The text to analyze.
        """
        self.text = text
        self.sentences = self._split_sentences()
        self.words = self._split_words()
    
    def _split_sentences(self):
        """Split the text into sentences using regular expressions."""
        sentence_pattern = r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s'
        return [s.strip() for s in re.split(sentence_pattern, self.text) if s.strip()]
    
    def _split_words(self):
        """Split the text into words using regular expressions."""
        word_pattern = r'\b\w+\b'
        return re.findall(word_pattern, self.text)
    
    def count_sentences(self):
        """Return the number of sentences in the text."""
        return len(self.sentences)
    
    def count_sentence_types(self):
        """Return the count of narrative, interrogative, and imperative sentences."""
        narrative = sum(1 for s in self.sentences if s.endswith('.'))
        interrogative = sum(1 for s in self.sentences if s.endswith('?'))
        imperative = sum(1 for s in self.sentences if s.endswith('!'))
        return narrative, interrogative, imperative
    
    def average_sentence_length(self):
        """Return the average length of sentences in characters (only words)."""
        total_length = sum(len(''.join(re.findall(r'\w', s))) for s in self.sentences)
        return total_length / len(self.sentences) if self.sentences else 0
    
    def average_word_length(self):
        """Return the average length of words in the text."""
        total_length = sum(len(word) for word in self.words)
        return total_length / len(self.words) if self.words else 0
    
    def count_smileys(self):
        """Return the number of smileys in the text based on the given pattern."""
        smiley_pattern = r'[:;]-*\(+|\)+|\[+|\]+'
        smileys = re.findall(smiley_pattern, self.text)
        return len(smileys)
    
    def get_lowercase_words_and_punctuation(self):
        """Return words starting with lowercase letters and punctuation marks."""
        lowercase_words = [word for word in self.words if word[0].islower()]
        punctuation = re.findall(r'[^\w\s]', self.text)
        return lowercase_words, punctuation
    
    def is_valid_mac_address(self, mac):
        """Check if the given string is a valid MAC address."""
        mac_pattern = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
        return bool(re.match(mac_pattern, mac))
    
    def count_words_starting_with_consonant(self):
        """Return the number of words starting with a consonant."""
        consonants = 'bcdfghjklmnpqrstvwxyz'
        return sum(1 for word in self.words if word[0].lower() in consonants)
    
    def find_words_with_double_letters(self):
        """Return words with double letters and their positions."""
        double_letter_pattern = r'\b\w*(\w)\1\w*\b'
        words_with_double = [(i, word) for i, word in enumerate(self.words) if re.search(double_letter_pattern, word)]
        return words_with_double
    
    def get_sorted_words(self):
        """Return the list of words in alphabetical order."""
        return sorted(self.words, key=str.lower)
    
    def get_all_analyses(self):
        """Выполняет все анализы текста и возвращает результаты в виде списка строк."""
        results = []
        results.append(f"Всего предложений: {self.count_sentences()}")
        narrative, interrogative, imperative = self.count_sentence_types()
        results.append(f"Повествовательные предложения: {narrative}")
        results.append(f"Вопросительные предложения: {interrogative}")
        results.append(f"Повелительные предложения: {imperative}")
        results.append(f"Средняя длина предложения: {self.average_sentence_length():.2f} символов")
        results.append(f"Средняя длина слова: {self.average_word_length():.2f} символов")
        results.append(f"Количество смайликов: {self.count_smileys()}")
        lowercase_words, punctuation = self.get_lowercase_words_and_punctuation()
        results.append(f"Слова, начинающиеся с маленькой буквы: {', '.join(lowercase_words)}")
        results.append(f"Знаки препинания: {', '.join(punctuation)}")
        results.append(f"Слова, начинающиеся с согласной: {self.count_words_starting_with_consonant()}")
        double_letter_words = self.find_words_with_double_letters()
        if double_letter_words:
            results.append("Слова с двойными буквами:")
            for pos, word in double_letter_words:
                results.append(f"  Позиция {pos}: {word}")
        else:
            results.append("Слов с двойными буквами не найдено.")
        sorted_words = self.get_sorted_words()
        results.append("Слова в алфавитном порядке:")
        results.append(', '.join(sorted_words))
        return results
