from collections import Counter, defaultdict

from data_structures import LinkedList
from search_helpers import normalise, load_postings_list, load_document_vector

ALPHA = 1.0
BETA = 0.75
THRESHOLD = 0


def get_relevant_docs(query, dictionary, vector_lengths, relevant_doc_ids,
                      document_vectors_dictionary, postings_file):
    query_vector = query_to_vector(query)
    new_query = rocchio_algorithm(query_vector, relevant_doc_ids,
                                  document_vectors_dictionary, ALPHA, BETA,
                                  postings_file)

    scores = defaultdict(float)
    for term, _ in new_query.items():
        if term not in dictionary:
            continue
        term_postings = Counter(
            load_postings_list(postings_file, dictionary, term))
        idf = dictionary[term][0]
        for doc_id, tf_d in term_postings:
            scores[doc_id] += tf_d * idf
    normalized_scores = sorted(((doc_id, score / vector_lengths[doc_id])
                                for doc_id, score in scores.items()),
                               key=lambda x: x[1],
                               reverse=True)
    relevant_docs = (x[0] for x in normalized_scores if x[1] > THRESHOLD)
    output = LinkedList()
    output.extend(relevant_docs)
    return output


def query_to_vector(query):
    return Counter(normalise(x) for x in query.split(' '))


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
