from lxml import html
import requests, nltk
from nltk.corpus import stopwords, wordnet
from nltk.stem.lancaster import LancasterStemmer
from collections import Counter


class Analyzer:

    def __init__(self):
        self.stopwords = set(stopwords.words('english')).union({'mouse', 'mice'})
        self.nouns = set(x.name().split('.', 1)[0] for x in wordnet.all_synsets('n'))
        self.stemmer = LancasterStemmer()
        self.animal_words = self.prepare_reference(self.animal_urls())
        self.computer_words = self.prepare_reference(self.computer_urls())

    @staticmethod
    def animal_urls():
        return ['https://en.wikipedia.org/wiki/Mouse',
                'https://en.wikipedia.org/wiki/Fancy_mouse',
                'https://en.wikipedia.org/wiki/Laboratory_mouse',
                'https://en.wikipedia.org/wiki/Rodent',
                'https://en.wikipedia.org/wiki/House_mouse',
                'https://en.wikipedia.org/wiki/Mus_(genus)',
                'https://en.wikipedia.org/wiki/Mousetrap']

    @staticmethod
    def computer_urls():
        return ['https://en.wikipedia.org/wiki/Computer_mouse',
                'https://en.wikipedia.org/wiki/Point_and_click',
                'https://en.wikipedia.org/wiki/Pointing_device_gesture',
                'https://en.wikipedia.org/wiki/Optical_mouse']

    def prepare_reference(self, urls):
        all_words = []
        for url in urls:
            page = requests.get(url)
            tree = html.fromstring(page.content)
            paragraphs = tree.xpath('//div[@class="mw-parser-output"]/p/text()')
            a_text = tree.xpath('//div[@class="mw-parser-output"]/p/a/text()')

            for p in paragraphs + a_text:
                tokens = nltk.word_tokenize(p)
                words = [self.stemmer.stem(t.lower())
                         for t in tokens
                         if t.isalpha()
                         and t.lower() not in self.stopwords
                         and t.lower() in self.nouns]
                all_words.extend(words)

        word_count = Counter(all_words)
        for word in word_count:
            word_count[word] = word_count[word]/len(all_words)

        return word_count

    def context(self, sentence):
        tokens = nltk.word_tokenize(sentence)
        words = [self.stemmer.stem(t.lower())
                 for t in tokens
                 if t.isalpha()
                 and t.lower() not in self.stopwords
                 and t.lower() in self.nouns]

        animal_count = sum([self.animal_words[w] for w in words])
        computer_count = sum([self.computer_words[w] for w in words])

        if animal_count > computer_count:
            print('animal')
            return 'animal'
        else:
            print('computer-mouse')
            return 'computer-mouse'

