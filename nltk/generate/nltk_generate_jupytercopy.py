import nltk
from nltk import PCFG
from nltk import CFG
from nltk.grammar import Nonterminal
from nltk.parse import ViterbiParser
from nltk.parse.generate import generate
from random import choices
from random import sample

MT = 1
N_SEN = 50
grammar_path = "../grammars/grammar_pcfg.txt"

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


if __name__ == "__main__":
    rules = open(grammar_path).read()
    grammar = PCFG.fromstring(rules)

    if MT == 1:
        sentences = [next(generate_corpus(grammar, Nonterminal('S'))) for s in range(500)]
        sentences = sample([s for s in sentences if 4 < len(s) < 15], N_SEN)
        for s in sentences:
            print(' '.join(s).lower())
        # print(sentences)
    
    if MT == 2:
        sentences = sample([s for s in generate(grammar, start=Nonterminal('S'), depth = 8, n = 100)], N_SEN)
        for s in sentences:
            print(' '.join(s).lower())
        # print(sentences)