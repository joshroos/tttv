import nltk
from nltk import word_tokenize
from nltk import sent_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet


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
    for sent in sentences:
        words = get_words(sent)
        pos = nltk.pos_tag(words)

        for i in pos:
            if i[1] not in used_tags:
                used_tags.append(i[1])
    return used_tags

txt = open('antonio.txt').read()
words = get_words(txt)
sentences = get_sentences(txt)
tags = sorted(pos_tags(sentences))

print("--Text Statistics --")
print("# words: \t", len(words))
print("# unique words: \t", len(set(words)))
print("average words length: \t", round(avg_len_words(words), 2))
print("unknown words: \t", get_unknown_words(set(words)))
print("hapaxes: \t", len(hapaxes(words)))
print("tags: \t", tags)
print("# tags: \t", len(tags))
print("-------------------------------")
print("# sentences: \t", len(sentences))
print("average sentence length: \t", round(avg_len_sent(sentences), 2))
print("longest sentence: \t", max([len(get_words(s)) for s in sentences]))



# tokens = word_tokenize(txt)
# print(words)
# print(sentences)


# words = [w.lower() for w in tokens]

# print(len(tokens))
# print(len(words))

# print(tokens[0:20])
# print(words[0:20])

# print(nltk.Text(tokens))

