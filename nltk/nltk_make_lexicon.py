import nltk
from nltk import word_tokenize
from nltk import sent_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk import CFG


def get_wordnet_pos(treebank_tag):

    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return ''


def get_words(txt):
    regex = RegexpTokenizer(r'\w+')
    return [w.lower() for w in regex.tokenize(txt)]


def get_sentences(txt):
    return sent_tokenize(txt)


def lemmatize_words(words):
    lemmatizer = WordNetLemmatizer()
    print(words)
    lemmas = lemmatizer.lemmatize(words[0], get_wordnet_pos(words[1]))
    print(lemmas)


def get_unknown_words(words):
    d = set(nltk.corpus.words.words())

    return [w for w in words if not w in d]


def avg_len_words(words):
    return sum([len(w) for w in words]) / len(words)


def avg_len_sent(sentences):
    length = 0
    for sent in sentences:
        length += len(get_words(sent))
    return length / len(sentences)


def hapaxes(words):
    return [w for w in words if words.count(w) == 1 ]


def pos_tags(sentences):
    used_tags = []
    tagged_words = []
    for sent in sentences:
        words = get_words(sent)
        pos = nltk.pos_tag(words)

        for i in pos:
            tagged_words.append(i)
            if i[1] not in used_tags:
                used_tags.append(i[1])
    return sorted(used_tags), tagged_words


def make_lexicon(tagged_words):
    lexicon = ""
    for word in tagged_words:
        string = "{} -> {}".format(word[1], word[0])
        string = string.replace('$', 'S')
        if string not in lexicon:
            lexicon = lexicon + string + '\n'
    return lexicon


txt = open('antonio.txt').read()
words = get_words(txt)
sentences = get_sentences(txt)
tags, tagged_words = pos_tags(sentences)

make_lexicon(tagged_words)