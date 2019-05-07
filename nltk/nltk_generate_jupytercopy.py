import nltk
from nltk import PCFG
from nltk import CFG
from nltk.grammar import Nonterminal
from nltk.parse import ViterbiParser
from nltk.parse.generate import generate
from random import choices

demo_pcfg = PCFG.fromstring("""
    S -> VP          [0.25]
    S -> NP VP       [0.75]
    
    VP -> V          [0.50]
    VP -> V NP       [0.50]
    
    NP -> D N        [0.40]
    NP -> N          [0.60]

    V -> 'read'      [0.75]
    V -> 'study'     [0.25]
    
    D -> 'the'       [1.00]
    
    N -> 'children'  [0.60]
    N -> 'books'     [0.40]
""")

demo_cfg = CFG.fromstring("""
    S -> VP
    S -> NP VP
    
    VP -> V
    VP -> V NP
    
    NP -> D N
    NP -> N

    V -> 'read'
    V -> 'study'
    
    D -> 'the'
    
    N -> 'children'
    N -> 'books'
""")

def generate_phrase(grammar, prod = None):
    if not prod:
        prod = grammar.start()
    if prod in grammar._lhs_index:
        # Non-terminals
        derivations = grammar._lhs_index[prod]
        try:
            probabilities = [d.prob() for d in derivations]
        except AttributeError:
            probabilities = None
        derivation = choices(derivations, probabilities)[0]      
        # print(derivation._rhs)     
        # input()
        for d in derivation._rhs:            
            yield from generate_phrase(grammar, d)
    elif prod in grammar._rhs_index:
        # Terminals
        yield str(prod)
        
def generate_corpus(grammar, prod = None):
    yield list(generate_phrase(grammar, prod))

rules = open('grammar_rules_reduced.txt').read()
grammar = CFG.fromstring(rules)
# sentence = next(generate_corpus(grammar))
# print(sentence)
sentences = [next(generate_corpus(grammar)) for s in range(10)]
print(sentences)