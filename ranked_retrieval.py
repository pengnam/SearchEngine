from collections import Counter, defaultdict
from nltk.corpus import wordnet

from data_structures import LinkedList
from search_helpers import normalise, load_postings_list, load_document_vector

# Variables for tuning
ALPHA = 1.0
BETA = 0.75
THRESHOLD = 0
QUERY_EXPANSION = True
RELEVANT_FEEDBACK = True


def get_relevant_docs(query, dictionary, vector_lengths, relevant_doc_ids,
                      document_vectors_dictionary, postings_file):
    query_vector = query_to_vector(query)
    if QUERY_EXPANSION:  # Requires non-normalized terms
        query_vector = query_expansion(query_vector)
    query_vector = normalized_vector(query_vector)
    if RELEVANT_FEEDBACK:  # Requires normalized terms
        query_vector = rocchio_algorithm(query_vector, relevant_doc_ids,
                                         document_vectors_dictionary, ALPHA, BETA,
                                         postings_file)
    scores = defaultdict(float)
    for term, factor in query_vector.items():
        if term not in dictionary:
            continue
        term_postings = load_postings_list(postings_file, dictionary, term)
        idf = dictionary[term][0]
        for doc_id, tf_d in term_postings:
            scores[doc_id] += factor * tf_d * idf
    normalized_scores = sorted(((doc_id, score / vector_lengths[doc_id])
                                for doc_id, score in scores.items()),
                               key=lambda x: x[1],
                               reverse=True)
    relevant_docs = (x[0] for x in normalized_scores if x[1] > THRESHOLD)
    output = LinkedList()
    output.extend(relevant_docs)
    return output


def query_to_vector(query):
    return Counter(x for x in query.strip().split(' '))


def normalized_vector(query_vector):
    result = defaultdict(float)
    for term, value in query_vector.items():
        result[normalise(term)] += value
    return result

def rocchio_algorithm(query, relevant_doc_ids, docs_vector, alpha, beta,
                      postings_file):

    relevant_docs_sum = Counter()
    for doc_id in relevant_doc_ids:
        relevant_docs_sum += load_document_vector(doc_id, postings_file,
                                                  docs_vector)
    relevant_docs_centroid = Counter({
        doc_id: beta * count / len(relevant_doc_ids)
        for doc_id, count in relevant_docs_sum.items()
    })

    normalized_query = Counter({k: alpha * v for k, v in query.items()})
    return dict(normalized_query + relevant_docs_centroid)


def query_expansion(query):
    result = {}
    for term, count in query.items():
        synonyms = wordnet.synsets(term)
        if len(synonyms) == 0:
            continue
        syn_term = synonyms[0]
        for synset in synonyms[1:]:
            factor = wordnet_score_factor(syn_term, synset)
            try:
                new_term = normalise(synset.lemmas()[0].name())
            except:
                continue
            if new_term in result:
                # We only find highest scoring synonyms
                continue
            result[new_term] = factor * count
    return dict(Counter(result) + Counter(query))


def wordnet_score_factor(first_word, word):
    result = first_word.wup_similarity(word)
    return result if result else 0
