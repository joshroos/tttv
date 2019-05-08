import nltk
from nltk import word_tokenize
from nltk import sent_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk import Tree
from nltk import CFG, PCFG
from nltk.parse import RecursiveDescentParser, ShiftReduceParser, BottomUpLeftCornerChartParser
from stanfordcorenlp import StanfordCoreNLP


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
    return [w for w in regex.tokenize(txt)]


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
    results = parser.parse_one(sentence)
    for tree in results:
        tree_found = True
        print(tree)
    if not tree_found:
        print(sentence, "Does not match the provided grammar.")
    print("--------------------------------------------------")
    return tree_found


def check_bool(parser, sentence):
    if isinstance(sentence, str):
        sentence = sentence.split()
    results = parser.parse_one(sentence)
    if results:
        for tree in results:
            print('True')
            return True
    print('False')
    return False


def extract_rules(sentences):
    nlp = StanfordCoreNLP('http://localhost', port=9000, timeout=30000)
    
    file_in = open('../grammars/grammar.txt', "w")
    for sentence in sentences:
        parsed = nlp.parse(sentence)
        t = Tree.fromstring(parsed)
        rules = t.productions()    
        for rule in rules:
            file_in.write(str(rule) + "\n")    
    file_in.close()


def write_grammar():
    file_in = open('../grammars/grammar.txt', "r")
    rules = file_in.read()
    rules = sorted(set(rules.split('\n')))
    file_in.close()
    file_out = open('../grammars/grammar_rules_2.txt', "w")
    for rule in rules:
        file_out.write(rule + '\n')
    file_out.close()


# def generate_sentences(cfg, n):
#     for sentence in generate(cfg, n=n):
#         print(' '.join(sentence))

if __name__ == "__main__":

    txt = open('../antonio_edited.txt').read()
    words = get_words(txt)
    sentences = get_sentences(txt)
    tags, tagged_words = pos_tags(sentences)

    #extract_rules(sentences)
    #write_grammar()

    rules = open('../grammars/grammar_pcfg.txt').read()
    print(rules)
    cfg1 = PCFG.fromstring(rules)
    cfg_1_parser = BottomUpLeftCornerChartParser(cfg1)

    num_trees = 0
    trees_found = 0
    print('here')

    for sentence in sentences:
        print(sentence)
        num_trees += 1
        if check_bool(cfg_1_parser, sentence):
            trees_found +=1