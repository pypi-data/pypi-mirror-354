from typing import List, Tuple, Optional
import importlib.resources
import math
import nltk
from collections import Counter

class PhonTactProb:
    """Provides functionality for analyzing phonotactic probabilities given a corpus
    The class is initialized with data from the nltk brown corpus

    This is needlessly large and painful, but a nice artifact to have.
    """

    def __init__(self,
                 corpus: Optional[List[str]] = None,
                 phonemes: Optional[List[str]] = None,
                 dictionary: Optional[str] = None):
        """Initialize an instance of PhonTactProb

        :param corpus: List of corpus strings (optional)
        :param phonemes: List of phoneme strings (optional)
        :param dictionary: Ignored if None, otherwise path to dictionary file (optional)
        """
        # set corpus
        if corpus is not None:
            self.corpus = corpus
        else:
            self.initialize_brown_corpus()
        # set phonemes
        if phonemes is not None:
            self.phonemes = phonemes
            self.c2i = {c: i for i, c in enumerate(self.phonemes, start=1)}
            self.i2c = {i: c for i, c in enumerate(self.phonemes, start=1)}
        else:
            self.initialize_english_phonemes()
        # set dictionary
        if dictionary is None:
            # Load dictionary.txt from package resources
            with importlib.resources.files('PhonTactProb').joinpath('data/dictionary.txt').open('r', encoding='utf-8') as f:
                self.data = f.readlines()
        else:
            with open(dictionary, 'r') as f:
                self.data = f.readlines()

        # the needed that will be filled by default processing functions
        self.wordlist = None
        self.positionally_encoded_wordlist = None
        self.wset = None
        self.positional_segmental_frequency = None
        self.ipa_positional_segmental_frequency = None
        self.positionally_encoded_biphones = None
        self.positional_segmental_biphone_frequency = None
        self.ipa_positional_segmental_biphone_frequency = None

        # building functions
        self.load_dictionary()
        self.corpuscounter = {w:f for w,f in Counter(self.corpus).items() if w in self.wset}
        self.positionally_encode_wordlist()
        self.positionally_encode_wordlist_biphones()
        self.calculate_positional_segmental_frequency()
        self.calculate_biphone_positional_segmental_frequency()

    def initialize_brown_corpus(self):
        """Sets self.corpus to the brown corpus"""
        import nltk
        from nltk.corpus import brown as b
        from nltk.corpus import stopwords

        # Check and download 'stopwords' only if needed
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')

        # Check and download 'brown' only if needed
        try:
            nltk.data.find('corpora/brown')
        except LookupError:
            nltk.download('brown')

        punctuation = ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=',
                       '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~', '``', "''", '--']

        # Combine punctuation and stopwords into a single list
        pun_stopwords = punctuation + stopwords.words('english')

        brown_words = [x.lower() for x in b.words()]
        # Remove punctuation and stopwords
        brown_words = [x for x in brown_words if x not in pun_stopwords]
        # Keep only alphabetic words longer than 1 character
        brown_words = list(filter(lambda x: x.isalpha() and len(x) > 1, brown_words))
        self.corpus = brown_words

    def initialize_english_phonemes(self):
        """Sets self.phonemes to a default set of english phonemes
        """
        self.phonemes = [
            # Consonants
            'b', 'd', 'f', 'g', 'h', 'dʒ', 'k', 'l', 'm', 'n', 'p', 'r', 's', 't', 'v', 'w', 'z', 'ʒ', 'tʃ', 'ʃ', 'θ', 'ð', 'ŋ', 'j',

            # Vowels
            'æ', 'eɪ', 'ɛ', 'iː', 'ɪ', 'aɪ', 'ɒ', 'oʊ', 'ʊ', 'ʌ', 'uː', 'ɔɪ', 'aʊ', 'ə', 'ɝ', 'ɚ', 'ɪə', 'eə', 'ʊə',

            #unlisted, added manually after checking
            'ɑ', 'ɔ', 'i', 'ɑː', 'ɔː',
            'æː', 'eɪː', 'ɛː', 'iː', 'ɪː', 'aɪː', 'ɒː', 'oʊː',
            'ʊː', 'ʌː', 'uː', 'ɔɪː', 'aʊː', 'əː', 'ɝː', 'ɚː',
            'ɪəː', 'eəː', 'ʊəː'
        ]
        self.c2i = {c: i for i, c in enumerate(self.phonemes, start = 1)}
        self.i2c = {i: c for i, c in enumerate(self.phonemes, start = 1)}

    def tokenize(self, word : str) -> Tuple[List[str], bool]:
        """
        Tokenizes a given string of IPA characters using the current vocabulary.

        This method attempts to segment the input string into the longest possible
        substrings that match entries in the vocabulary (`self.c2i`). If any part
        of the string cannot be matched, the remainder of the unmatched string is appended to
        the output and the method returns `False`.

        Args:
            word (str): A string of IPA characters to be tokenized.

        Returns:
            Tuple[List[str], bool]: A tuple where the first element is a list of
            tokenized segments (or partial segments), and the second element is
            a boolean indicating whether the tokenization was completely successful.
        """
        encoded = []
        max_len = max([len(x) for x in self.c2i.keys()])
        while word:
            matched = False
            for i in range(min(max_len, len(word)), 0, -1):  # Try substrings from max_len to 1
                chunk = word[:i]
                if chunk in self.c2i:
                    encoded.append(self.c2i[chunk])
                    word = word[i:]
                    matched = True
                    break
            if not matched:
                return encoded + [word], False

        return encoded, True

    def load_dictionary(self):
        """
        Loads a dictionary from self.dictionary for use establishing probabilities
        """
        wordlist = self.data
        self.wordlist = [(x.strip().split('\t')[0], x.strip().split('\t')[1]) for x in wordlist]
        self.wset = set([w for w,_ in self.wordlist])

    def positionally_encode_wordlist(self):
        """
        tokenize the wordlist into its positionally encoded format, each phoneme marked by position.p1.p2...
        """
        encoded = []
        for w,i in self.wordlist:
            e, success = self.tokenize(i)
            assert success, f"{e[-1]} contains IPA not found in your vocabulary: {e[-1][0]}"
            encoded.append((w, e))
        self.positionally_encoded_wordlist = [(w, [f"{n}.{c}"for n,c in enumerate(i, start=1)]) for w,i in encoded]
        self.wset = set([w[0] for w in encoded])

    def positionally_encode_wordlist_biphones(self):
        encoded = []
        for w, i in self.wordlist:
            e, success = self.tokenize(i)
            assert success, f"{e[-1]} contains IPA not found in your vocabulary: {e[-1][0]}"
            encoded.append((w, [f"{i}.{c[0]}.{c[1]}" for i, c in enumerate(nltk.bigrams(e), start=1)]))
        self.positionally_encoded_biphones = encoded

    def calculate_positional_segmental_frequency(self):
        """
        Calculates positional segmental frequency into self.positional_segmental_frequency
        from self.positionalencodedwordlist and self.corpuscounter
        """
        segmental_dictionary = {}
        length_dictionary = {}  # tracks all phoneme sequence lengths
        for w, e in self.positionally_encoded_wordlist:
            if len(e) not in length_dictionary:
                if w in self.corpuscounter:
                    length_dictionary[len(e)] = [math.log10(self.corpuscounter[w])]
            else:
                if w in self.corpuscounter:
                    length_dictionary[len(e)].append(math.log10(self.corpuscounter[w]))
            for s in e:
                if s not in segmental_dictionary:
                    if w in self.corpuscounter:
                        segmental_dictionary[s] = [math.log10(self.corpuscounter[w])]
                else:
                    if w in self.corpuscounter:
                        segmental_dictionary[s].append(math.log10(self.corpuscounter[w]))

        maxlen = max(length_dictionary.keys())

        positional_segmental_frequency = {}
        for s, w in segmental_dictionary.items():
            # get freq total of encs with len below position
            total = 0
            for i in range(int(s.split('.')[0]), maxlen + 1):
                total += sum(length_dictionary[i])
            positional_segmental_frequency[s] = sum(w) / total
        self.positional_segmental_frequency = positional_segmental_frequency
        self.ipa_positional_segmental_frequency = {}
        for k, v in positional_segmental_frequency.items():
            self.ipa_positional_segmental_frequency[f"{self.i2c[int(k.split('.')[1])]}{k.split('.')[0]}"] = v

    def calculate_biphone_positional_segmental_frequency(self):
        """
        Calculates positional segmental frequency into self.positional_segmental_frequency
        from self.positionalencodedbiphones and self.corpuscounter
        """
        segmental_biphones_dictionary = {}
        length_biphones_dictionary = {}  # tracks all biphone sequence lengths
        for w, e in self.positionally_encoded_biphones:
            if len(e) not in length_biphones_dictionary:
                if w in self.corpuscounter:
                    length_biphones_dictionary[len(e)] = [math.log10(self.corpuscounter[w])]
                else:
                    if w in self.corpuscounter:
                        length_biphones_dictionary[len(e)].append(math.log10(self.corpuscounter[w]))
            for s in e:
                if s not in segmental_biphones_dictionary:
                    if w in self.corpuscounter:
                        segmental_biphones_dictionary[s] = [math.log10(self.corpuscounter[w])]
                    else:
                        if w in self.corpuscounter:
                            segmental_biphones_dictionary[s].append(math.log10(self.corpuscounter[w]))
        maxlen = max(length_biphones_dictionary.keys())

        positional_segmental_biphone_frequency = {}
        for s, w in segmental_biphones_dictionary.items():
            total = 0
            for i in range(int(s.split('.')[0]), maxlen + 1):
                total += sum(length_biphones_dictionary[i])
            positional_segmental_biphone_frequency[s] = sum(w) / total
        self.positional_segmental_biphone_frequency = positional_segmental_biphone_frequency

        ipa_positional_segmental_biphone_frequency = {}
        for k, v in positional_segmental_biphone_frequency.items():
            ipa_positional_segmental_biphone_frequency[
                f"{self.i2c[int(k.split('.')[1])]}{self.i2c[int(k.split('.')[2])]}{k.split('.')[0]}"] = v
        self.ipa_positional_segmental_biphone_frequency = ipa_positional_segmental_biphone_frequency

    def compute_phonotactic_probability(self, ipa:str) -> dict[str, dict[str, list[tuple[str, float]]]]:
        """
        Compute phonotactic probabilities for a space-separated string of IPA words.

        Given a string of IPA-transcribed words separated by spaces, this method returns a
        dictionary where each key is a word and each value is another dictionary containing:

            - 'phonemes': A list of tuples (phoneme, phonotactic probability)
            - 'biphones': A list of tuples (biphone, phonotactic probability)

        Returns:
            dict: A dictionary structured as:
                {
                    word1: {
                        'phonemes': [(phon1, prob1), (phon2, prob2), ...],
                        'biphones': [(biph1, prob1), (biph2, prob2), ...]
                    },
                    word2: {...},
                    ...
                }
        """
        result = {}
        split_sentence = ipa.split()
        for word in split_sentence:
            e, success = self.tokenize(word)
            assert success, f"{e[-1]} contains IPA not found in your vocabulary: {e[-1][0]}"
            phonemes = [f"{self.i2c[c]}{i}" for i, c in enumerate(e, start=1)]
            biphones = [f"{self.i2c[c[0]]}{self.i2c[c[1]]}{i}" for i, c in enumerate(nltk.bigrams(e), start=1)]
            result[word] = {
                'phonemes': [(p, self.ipa_positional_segmental_frequency.get(p, 0)) for p in phonemes],
                'biphones': [(b, self.ipa_positional_segmental_biphone_frequency.get(b, 0)) for b in biphones]
            }
        return result