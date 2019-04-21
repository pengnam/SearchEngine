This is the README file for A0164710M, A0149787E, A0164178X, A0167354Y.

== Python Version ==

I'm using Python Version <3.4> for this assignment.

== General Notes about this assignment ==

Auxiliary Modules:
1. Data Structures:
  We have a data structure module to hold all the important data structures, such
  as a linkedlist data structure and a list node data structure.
2. Boolean Retrieval
  For all boolean retrieval code
3. Phrasal retrieval
  For all phrasal retrieval code
4. Ranked retrieval
  For all ranked retrieval code
5. Search Helpers
  Functions used to retrieve items from the dictionary file, get_weighted_tf, or
  to normalise tokens.

To run index.py, please install joblib by running `pip install joblib`


This assignment contains the code for both:

1. Indexing
We stored 4 different items in the index.
For all these dictionaries except the vector lengths dictionary, instead of
storing the actual data in the dictionary, we stored the information that will
allow us to retrieve the information from the posting list.

A. Positional Index
Content: Dictionary of tokens, where each token is mapped to a linkedlist of
tuples, each consisting of document id and a linkedlist to positions of the
token in that document.
Type: Dict[str, LinkedList[Tuple[str, LinkedList[int]]]]
Purpose: For phrasal queries

B. TF-IDF Dictionary
Content: Dictionary of tokens to the tf values for each document id.
Type: Dict[str, LinkedList[Tuple[str, float]]]
Purpose: Used for computing the tf-idf values

C. Vector Lengths
Content: Contains all the vector lengths for each token
Type: Dict[str, float]
Purpose: Used for computing ranking scores using cosine similarity.

D. Document vectors (for relevant query [bonus])
Content: Dictionary of docID to sparse vector
Type: Dict[str, Dict[str, int]]
Purpose: For relevant query


2. Searching:
Searching will be described in greater detail in BONUS document.
We broke the searching into three parts: ranked retrieval, boolean retrieval
(which includes phrasal matching), and relevant feedback.

In essence, the searching is done through the following method:
1) Ranked retrieval is performed on the text to retrieve a ranked list of
document ids
2) Boolean retrieval is performed to retrieve all documents that match the
query. (free text are treated as OR queries).


Results are retrieved according to the following priorities:
1. Matching boolean queries
2. Having a ranked score past a certain threshold

The resultant list contains documents that satisfy either of the two criteria
above, and documents in list are ranked by the first priority before the second
priority.

We then implemented a threshold for the resultant list to limit the number of
documents returned.


Relevant feedback is used to supplement ranked retrieval, and will be described
in the BONUS document.


== Notable Engineering Features ==
Indexing is implemented using parallel techniques. We reduced the time from 75
minutes to 7 minutes by parallelizing

We tried different ways to index to process phrasal queries. The first method
was to implement bitriword indexing since phrases can only be of a maximum size
3.
We decided to use positional indexing in the end as the size of the postings
and dictionary files using bitriword dictionary was more than 10 times larger
than using positional index.





== Breakdown of work ==
A0164710M: Helped with initial indexing, worked on phrasal retrieval,
ranked retrieval
A0149787E:: Implemented and optimized indexing, testing, submission
A0164178X: Implemented all bonus parts, ranked retrieval, submission
A0167354Y: Implemented boolean retrieval, integrating components, testings




== Files included with this submission ==


== Statement of individual work ==

Please initial one of the following statements.

[X] We, A0164710M, A0164710M, A0149787E, A0164178X, A0167354Y, certify that we
have followed the CS 3245 Information Retrieval class guidelines for homework
assignments. In particular, we expressly vow that we have followed the Facebook
rule in discussing with others in doing the assignment and did not take notes
(digital or printed) from the discussions.

[ ] I, A0000000X, did not follow the class rules regarding homework
assignment, because of the following reason:


== References ==
We consulted from Python documentation websites, especially the following pages:
1. Pickle documentation: https://docs.python.org/3/library/pickle.html
2. functools documentation: https://docs.python.org/3/library/functools.html
3. itertools documentation: https://docs.python.org/3/library/itertools.html
