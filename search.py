"""
Processes search queries
"""

import csv
import getopt
import sys
import itertools
from itertools import chain

from data_structures import TokenType, QueryType
from ranked_retrieval import get_relevant_docs
from boolean_retrieval import perform_boolean_query
from search_helpers import normalise, load_dictionaries


def usage():
    """
    Prints the usage message.
    """
    print("usage: " + sys.argv[0] +
          " -d dictionary-file -p postings-file -q file-of-queries" +
          " -o output-file-of-results")


####################
# Query processing #
####################


def process_query(dictionary, vector_lengths, postings_file_location,
                  file_of_queries_location, document_vectors_dictionary,
                  file_of_output_location):
    """
    Process the query in the query file.
    """
    with open(file_of_queries_location, 'r') as query_file, \
            open(postings_file_location, 'rb') as postings_file, \
            open(file_of_output_location, 'w') as output_file:
        query, *relevant_doc_ids = list(query_file)
        query_type, tokens = parse_query(query)
        relevant_doc_ids = [x.strip() for x in relevant_doc_ids]
        query_phrase = " ".join(itertools.chain.from_iterable(
            [(x if token_type is TokenType.PHRASE else [x]) for token_type, x in tokens]))
        result = get_relevant_docs(query_phrase, dictionary, vector_lengths,
                                   relevant_doc_ids,
                                   document_vectors_dictionary, postings_file)
        if query_type is QueryType.BOOLEAN:
            boolean_results = set(
                perform_boolean_query(tokens, dictionary, postings_file))
            # Sort documents that satisfy boolean query to be the top results.
            relevant_boolean = []
            relevant_non_boolean = []
            for doc_id in result:
                if doc_id in boolean_results:
                    relevant_boolean.append(doc_id)
                else:
                    relevant_non_boolean.append(doc_id)
            relevant_boolean.extend(relevant_non_boolean)
            result = relevant_boolean
        postings = str(result)
        output_file.write(postings + "\n")


def parse_query(query):
    """
    Parses query.

    Clarification from Zhao Jin:
    The queries could be in the form of A B C, A AND B AND C, "A B" AND C,
    but not A B AND C.

    Note that the query is actually a row in a CSV document with
    space delimiter and double quote as the quote character.
    """
    # import pdb; pdb.set_trace()
    tokens = list(csv.reader([query], delimiter=' ', quotechar='"'))[0]
    if 'AND' in tokens:
        return (QueryType.BOOLEAN,
                [parse_token(token) for token in tokens if token != 'AND'])
    return QueryType.FREE_TEXT, [parse_token(token) for token in tokens]


def parse_token(token):
    """
    Parses the given token by normalising it.
    """
    if ' ' in token:
        return TokenType.PHRASE, [normalise(word) for word in token.split()]
    return TokenType.NON_PHRASE, normalise(token)


# def process_query(query, dictionary, postings_file, output_file):
#     """
#     Calculates the cosine scores of the documents, get 10 documents with the
#     highest scores and writes to file
#     """
#    scores = Counter()
#    lengths = dictionary["LENGTHS"]
#    weighted_tfs = get_weighted_tfs(parse(query))
#    for term, tf_q in list(weighted_tfs.items()):
#        if term not in dictionary:
#            continue
#        postings = load_postings(postings_file, dictionary, term)
#        idf = dictionary[term][0]
#        for doc, tf_d in postings:
#            scores[doc] += tf_d * tf_q * idf
#    for doc in list(scores.keys()):
#        scores[doc] = float(scores[doc]) / lengths[doc]
#
#    postings = " ".join(str(x) for x in retrieve_top_ten_scores(scores))
#    output_file.write(postings + "\n")


def main():
    """
    The main function of this file.
    """
    dictionary_file = postings_file = file_of_queries = file_of_output = ""

    try:
        opts, _ = getopt.getopt(sys.argv[1:], 'd:p:q:o:')
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-d':
            dictionary_file = arg
        elif opt == '-p':
            postings_file = arg
        elif opt == '-q':
            file_of_queries = arg
        elif opt == '-o':
            file_of_output = arg
        else:
            assert False, "unhandled option"

    if any(x == "" for x in
           [dictionary_file, postings_file, file_of_queries, file_of_output]):
        usage()
        sys.exit(2)

    dictionary, document_vectors_dictionary, vector_lengths = \
        load_dictionaries(dictionary_file)

    process_query(dictionary, vector_lengths, postings_file, file_of_queries,
                  document_vectors_dictionary, file_of_output)


if __name__ == "__main__":
    main()
