import nltk
from nltk import word_tokenize
from nltk import sent_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer

def get_words(txt):
    regex = RegexpTokenizer(r'\w+')
    return [w.lower() for w in regex.tokenize(txt)]

def get_sentences(txt):
    return sent_tokenize(txt)


def lemmatize_words(words):
    lemmatizer = WordNetLemmatizer()
    word = 'times'
    lemmas = lemmatizer.lemmatize(word, 'v')
    print(lemmas)


def get_unknown_words(words):
    d = set(nltk.corpus.words.words())

    return [w for w in words if not w in d]

def avg_len_words(words):
    return sum([len(w) for w in words]) / len(words)

def avg_len_sent(sentences):
    length = 0
    for sent in sentences:
        length = len(get_words(sent))
        if length > 40:
            print(nltk.pos_tag(get_words(sent)))
    return length / len(sentences)

def hapaxes(words):
    return [w for w in words if words.count(w) == 1 ]

txt = open('antonio.txt').read()
words = get_words(txt)
sentences = get_sentences(txt)

print("--Text Statistics --")
print("# words: \t", len(words))
print("# unique words: \t", len(set(words)))
print("average words length: \t", round(avg_len_words(words), 2))
print("hapaxes: \t", hapaxes(words))
print("-------------------------------")
print("# sentences: \t", len(sentences ))
print("average sentence length: \t", round(avg_len_sent(sentences), 2))
print(get_unknown_words(set(words)))


# tokens = word_tokenize(txt)
# print(words)
# print(sentences)


# words = [w.lower() for w in tokens]

# print(len(tokens))
# print(len(words))

# print(tokens[0:20])
# print(words[0:20])

# print(nltk.Text(tokens))

