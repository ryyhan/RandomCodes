import math
from collections import defaultdict
import re

class BM25Okapi:
    """
    A class for performing BM25 keyword search on a corpus of documents.

    BM25 is a ranking function used to estimate the relevance of documents to a
    given search query. It is based on the probabilistic retrieval framework.
    """
    
    # Free parameters for the BM25 formula.
    # k1 is for term frequency saturation. A higher value means TF plays a larger role.
    # b is for document length normalization. 0 means no normalization, 1 means full normalization.
    def __init__(self, corpus, k1=1.5, b=0.75):
        """
        Initializes the BM25 model.

        Args:
            corpus (list of str): A list of documents to be indexed.
            k1 (float, optional): BM25 parameter. Defaults to 1.5.
            b (float, optional): BM25 parameter. Defaults to 0.75.
        """
        self.corpus = corpus
        self.k1 = k1
        self.b = b
        self.doc_count = len(corpus)
        self.doc_lengths = []
        self.avg_doc_length = 0
        self.doc_freqs = []
        self.idf = {}
        self.doc_term_freqs = []

        self._initialize()

    def _tokenize(self, text):
        """
        Simple tokenizer that splits text into lowercased words.
        
        Args:
            text (str): The input string.

        Returns:
            list of str: A list of tokens.
        """
        # Use regex to find all words, convert to lower case
        return re.findall(r'\w+', text.lower())

    def _initialize(self):
        """
        Pre-processes the corpus to calculate necessary statistics for BM25.
        This includes document lengths, term frequencies, and IDF scores.
        """
        # Temporary storage for document frequency calculation
        df = defaultdict(int)
        total_doc_length = 0

        # Iterate through each document in the corpus
        for doc in self.corpus:
            tokens = self._tokenize(doc)
            self.doc_lengths.append(len(tokens))
            total_doc_length += len(tokens)
            
            # Calculate term frequencies for the current document
            term_freqs = defaultdict(int)
            for token in tokens:
                term_freqs[token] += 1
            self.doc_term_freqs.append(term_freqs)
            
            # Update document frequencies (count of docs containing a term)
            for token in set(tokens):
                df[token] += 1

        self.avg_doc_length = total_doc_length / self.doc_count if self.doc_count > 0 else 0
        
        # Calculate IDF for each term in the vocabulary
        for term, freq in df.items():
            # Standard IDF formula
            self.idf[term] = math.log((self.doc_count - freq + 0.5) / (freq + 0.5) + 1.0)

    def get_scores(self, query):
        """
        Calculates the BM25 scores for a given query against all documents.

        Args:
            query (str): The search query.

        Returns:
            list of float: A list of BM25 scores, one for each document.
        """
        query_tokens = self._tokenize(query)
        scores = [0] * self.doc_count

        for i in range(self.doc_count):
            score = 0
            doc_len = self.doc_lengths[i]
            term_freqs = self.doc_term_freqs[i]
            
            for term in query_tokens:
                if term not in term_freqs:
                    continue
                
                freq = term_freqs[term]
                
                # Calculate the term frequency component of BM25
                numerator = freq * (self.k1 + 1)
                denominator = freq + self.k1 * (1 - self.b + self.b * (doc_len / self.avg_doc_length))
                
                # Combine with IDF to get the score for this term
                score += self.idf.get(term, 0) * (numerator / denominator)
            
            scores[i] = score
            
        return scores

    def get_top_n(self, query, n=5):
        """
        Gets the top n most relevant documents for a query.

        Args:
            query (str): The search query.
            n (int, optional): The number of top documents to return. Defaults to 5.

        Returns:
            list of tuple: A list of (document, score) tuples for the top n documents.
        """
        scores = self.get_scores(query)
        
        # Pair scores with their corresponding documents
        doc_scores = list(zip(self.corpus, scores))
        
        # Sort documents by score in descending order
        doc_scores.sort(key=lambda x: x[1], reverse=True)
        
        return doc_scores[:n]

# --- Example Usage ---
if __name__ == '__main__':
    # A sample collection of documents
    corpus = [
        "The quick brown fox jumps over the lazy dog",
        "A lazy brown dog naps under the tree",
        "The quick fox is a brown fox",
        "Never underestimate the power of a good book",
        "London is the capital of Great Britain",
        "The quick brown fox and the lazy dog are friends",
        "The stock market is volatile today, with tech stocks leading the decline",
        "Investing in the stock market requires careful research and a long-term strategy"
    ]

    # Create a BM25 object
    bm25 = BM25Okapi(corpus)

    # --- Test Queries ---
    print("--- Example 1: Query 'quick brown fox' ---")
    query1 = "quick brown fox"
    top_n_results1 = bm25.get_top_n(query1, n=3)

    for doc, score in top_n_results1:
        print(f"Score: {score:.4f}\tDoc: {doc}")

    print("\n" + "="*50 + "\n")
    
    print("--- Example 2: Query 'stock market' ---")
    query2 = "stock market"
    top_n_results2 = bm25.get_top_n(query2, n=3)

    for doc, score in top_n_results2:
        print(f"Score: {score:.4f}\tDoc: {doc}")
        
    print("\n" + "="*50 + "\n")
    
    print("--- Example 3: Query 'lazy dog' ---")
    query3 = "lazy dog"
    top_n_results3 = bm25.get_top_n(query3, n=3)

    for doc, score in top_n_results3:
        print(f"Score: {score:.4f}\tDoc: {doc}")
