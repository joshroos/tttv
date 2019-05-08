import nltk_main as nl
import nltk
from nltk import Tree
from stanfordcorenlp import StanfordCoreNLP

txt = open('../antonio_edited.txt').read()

sentences = nl.get_sentences(txt)

def extract_rules(sentences):
    nlp = StanfordCoreNLP('http://localhost', port=9000, timeout=30000)
    file_in = open('../grammars/grammar_pcfg.txt', "w")
    all_rules = []
    all_tags = []
    count_tags = {}
    for sentence in sentences:
        parsed = nlp.parse(sentence)
        t = Tree.fromstring(parsed)
        rules = t.productions()
        for rule in rules:
            all_rules.append(str(rule))
            all_tags.append(str(rule)[:5])
    unique_rules = sorted(set(all_rules))
    print(sorted(set(all_tags)))
    for tag in sorted(set(all_tags)):
        count = all_tags.count(tag)
        count_tags[tag] = count
    print(count_tags)
    for rule in unique_rules:
        count = all_rules.count(rule)
        count_tag = count_tags[rule[:5]]
        file_in.write(rule + ' [{}]'.format(count/count_tag) + '\n')
    file_in.close()


def write_grammar():
    file_in = open('../grammars/grammar_pcfg.txt', "r")
    rules = file_in.read()
    rules = sorted(set(rules.split('\n')))
    file_in.close()
    file_out = open('../grammars/grammar_rules_pcfg.txt', "w")
    for rule in rules:
        file_out.write(rule + '\n')
    file_out.close()


extract_rules(sentences)
