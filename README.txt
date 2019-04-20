This is the README file for A0164710M, A0149787E, A0164178X, A0167354Y.

== Python Version ==

I'm using Python Version <3.4> for
this assignment.

== General Notes about this assignment ==

Auxilliary Modules:
1. Data Structures:
We have a data structure module to hold all the important data structures, such as a linkedlist data structure and a list node data structure.
2. Boolean Retrieval
For all boolean retrieval code
3. Phrasal retrieval
For all phrasal retrieval code
4. Ranked retrieval
For all ranked retrieval code
5. Search Helpers
Functions used to retrieve items from the dictionary file, get_weighted_tf, or to normalise.


This assignment contains the code for both:

1. Indexing
We stored 4 different items in the index.
For all these dictionaries except the vector lengths dictionary,  instead of storing the actual data in the dictionary, we stored the information that will allow us to retrieve the information from the posting list.

A. Positional Index
Content: Dictionary of tokens, where each token is linked to a linkedlist of document ids that each have a linkedlist to positions of the token in the document
Type: Dict[str, LinkedList[Tuple[str, LinkedList[int]]]]
Purpose: For phrasal queries

B. TF-IDF Dictionary
Content: Dictionary of tokens to the tf values for each document
Type: Dict[str, LinkedList[Tuple[str, float]]]
Purpose: Used for computing the tf-idf values


C. Vector Lengths
Content: Contains all the vector lengths for each token
Type: Dict[str, float]
Purpose: Used for computing ranking scores

D. Document vectors (for relevant query [bonus])
Content: Dictionary of docID to sparse vector
Type: Dict[str, Dict[str, int]]
Purpose: For relevant query


2. Searching:
Searching will be described in greater detail in BONUS document.
We broke the searching into three parts: ranked retrieval, boolean retrieval (which includes phrasal matching), and relevant feedback..

In essence, the searching is done through the following method:
1) Ranked retrieval is performed on the text to retrieved a ranked list of document ids
2) Boolean retrieval is performed to retrieve all documents that match the query. (free text are treated or OR queries).


Results are retrieved according to the following priorities:
1. Matching boolean queries
2. Having a ranked score pass a certain threshold

The resultant list contains documents that satisfy either of the two criteria above, and documents in list are ranked by the first priority before the second priority.

We then implemented a threshold for the resultant list to limit the number of documents returned.


Relevant feedback is used to supplement ranked retrieval, and will be described in the BONUS document.


== Files included with this submission ==


== Statement of individual work ==

Please initial one of the following statements.

[X] We, A0164710M, A0164710M, A0149787E, A0164178X, A0167354Y,, certify that we have followed the CS 3245 wenformation
Retrieval class guidelines for homework assignments.  wen particular, we
expressly vow that we have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.

[ ] I, A0000000X, did not follow the class rules regarding homework
assignment, because of the following reason:




Email: e0148752@u.nus.edu
