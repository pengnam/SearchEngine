"""
Contains helper methods for search.py
"""
import pickle

from math import log
from collections import Counter
from functools import lru_cache

from nltk.stem.porter import PorterStemmer

from data_structures import LinkedList

#######################
# Parsing and loading #
#######################


def get_weighted_tf(count, base=10):
    """
    Calculates the weighted term frequency
    using the 'logarithm' scheme.
    """
    return log(base * count, base)


def get_weighted_tfs(counts):
    """
    Calculate the weighted term frequencies.
    """
    return {k: get_weighted_tf(v) for k, v in counts.items()}


@lru_cache(maxsize=None)
def normalise(token):
    """
    Returns a normalised token. Normalised tokens are cached for performance
    """
    token = token.lower()
    return PorterStemmer().stem(token)


def load_document_vector(doc_id, postings_file, document_vector_dictionary):
    """
    Loads the document vectors for the given doc_id from the postings file.

    Returns a Counter where the key is token and the value is the occurrence.
    """
    if doc_id not in document_vector_dictionary:
        return Counter()
    offset, length = document_vector_dictionary[doc_id]
    postings_file.seek(offset)
    pickled = postings_file.read(length)
    return pickle.loads(pickled)


def load_postings_list(postings_file, dictionary, token):
    """
    Loads postings list from postings file using the location provided
    by the dictionary.

    Returns an empty LinkedList if token is not in dictionary.
    """
    if token not in dictionary:
        return LinkedList()
    _, (offset, length), _ = dictionary[token]
    postings_file.seek(offset)
    pickled = postings_file.read(length)
    return pickle.loads(pickled)


def load_positional_index(postings_file, dictionary, token):
    """
    Loads positional index from postings file using the location provided
    by the dictionary.

    Returns an empty LinkedList if token is not in dictionary.
    """
    if token not in dictionary:
        return LinkedList()
    _, _, (offset, length) = dictionary[token]
    postings_file.seek(offset)
    pickled = postings_file.read(length)
    return pickle.loads(pickled)


def load_dictionaries(dictionary_file_location):
    """
    Loads dictionary from dictionary file location.
    Returns a tuple of (dictionary, document_vector_dictionary, vector_lengths)
    """
    with open(dictionary_file_location, 'rb') as dictionary_file:
        return pickle.load(dictionary_file)
