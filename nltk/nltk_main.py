import nltk
from nltk import word_tokenize
from nltk import sent_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk import CFG
from nltk.parse import RecursiveDescentParser, ShiftReduceParser, BottomUpLeftCornerChartParser


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
            if i[0] == 'antonio' or i[0] == 'canova':
                i = (i[0], 'NNP')
            tagged_words.append(i)
            if i[1] not in used_tags:
                used_tags.append(i[1])
    return sorted(used_tags), tagged_words


def make_lexicon(tagged_words):
    lexicon = ""
    for word in tagged_words:
        string = "{} -> '{}'".format(word[1], word[0])
        string = string.replace('$', 'S')
        if string not in lexicon:
            lexicon = lexicon + string + '\n'
    return lexicon


def print_statistics(words, sentences, tags):
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


def check_sentence(parser, sentence):
    print("--------------------------------------------------")
    print("Checking if provided sentence matches the grammar:")
    print(sentence)
    if isinstance(sentence, str):
        sentence = sentence.split()
        print("here")
    tree_found = False
    results = parser.parse(sentence)
    for tree in results:
        tree_found = True
        print(tree)
    if not tree_found:
        print(sentence, "Does not match the provided grammar.")
    print("--------------------------------------------------")
    return tree_found


txt = open('antonio.txt').read()
words = get_words(txt)
sentences = get_sentences(txt)
tags, tagged_words = pos_tags(sentences)
lexicon = make_lexicon(tagged_words)
rules = open('grammar_rules.txt').read()
cfg1 = CFG.fromstring(rules + lexicon)
cfg_1_parser = BottomUpLeftCornerChartParser(cfg1)

tree = check_sentence(cfg_1_parser, 'the count would be very angry')
tree = check_sentence(cfg_1_parser, 'antonio was a puny lad and not strong enough to work')
