import nltk
import sys
import os
import re
import math
import argparse
from ascii_graph import Pyasciigraph

#directory = None #

def main():
    # parsing the arguments
    args = parse_args()
    if args.file[-4:] == '.txt':
        pass
    else:
        print('Należy podać jako argument plik .txt.')
        sys.exit()

    # Read and tokenize words from the file
    tokens = read_n_tokenize(args.file, args.l)

    top = top_words(tokens,args.n)

    graph = Pyasciigraph()
    for line in graph.graph('histogram', top):
        print(line)


def parse_args():
    """
    Ustala wymagane i opcjonalne argumenty, a następnie
    zwraca strukturę, dla której są to atrybuty.
    """
    parser = argparse.ArgumentParser(description='to jest opis')
    parser.add_argument('file', help='name of file to analyse')
    parser.add_argument('-n', help='number of words to include in histogram', type=int, default=10)
    parser.add_argument('-l', help='minimum length of a word in histogram', type=int, default=0)
#    parser.add_argument('-ignored', help='list of ignored words', type=list)
    return parser.parse_args()

def read_n_tokenize(file_name, l):
    """
    Czyta plik, a następnie dokonuje tonekizacji - podziału na pojedyncze słowa. Zwracana jest lista słów.
    """
    # If filename specified, read sentence from file
    contents=''
    with open(file_name, mode='r', encoding='utf8') as f:
        contents = f.read()

    tokens = nltk.word_tokenize(contents)
    tokens = [word for word in tokens if re.search('[a-zA-Z]|ą|Ą|ć|Ć|ę|Ę|ł|Ł|ń|Ń|ó|Ó|ś|Ś|ź|Ź|ż|Ż+', word,re.UNICODE)]
    tokens = [word for word in tokens if len(word) > l]
    return tokens

def top_words(tokens, n):
    """
    Zwraca listę tupli n najczęściej użytych słów, gdzie pierwszym elementem tupla jest słow, a drugim ilość
    pojawień się w tekście.
    """
    words = set(tokens)
    distribution = dict()
    for word in words:
        distribution[word] = tokens.count(word)
        
    top = list(sorted(distribution.items(), key=lambda x: x[1], reverse=True))
    return top[:n]


if __name__ == "__main__":
    main()
