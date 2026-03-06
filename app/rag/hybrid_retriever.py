from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from rank_bm25 import BM25Okapi
import numpy as np


def reciprocal_rank_fusion(results_list, k=60):
    scores = {}

    for results in results_list:
        for rank, doc in enumerate(results):
            doc_id = id(doc)
            scores[doc_id] = scores.get(doc_id, 0) + 1 / (k + rank)

    sorted_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    # Map back to documents
    id_to_doc = {id(doc): doc for results in results_list for doc in results}

    return [id_to_doc[doc_id] for doc_id, _ in sorted_docs]


def get_hybrid_retriever():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vectorstore = Chroma(
        persist_directory="chroma_db",
        embedding_function=embeddings
    )

    vector_docs = vectorstore.get()["documents"]

    # Convert to Document objects
    documents = [
        Document(page_content=doc) for doc in vector_docs
    ]

    # Prepare BM25
    tokenized_corpus = [doc.page_content.split() for doc in documents]
    bm25 = BM25Okapi(tokenized_corpus)

    def hybrid_search(query, top_k=3):
        # Vector search
        vector_results = vectorstore.similarity_search(query, k=top_k)

        # BM25 search
        tokenized_query = query.split()
        bm25_scores = bm25.get_scores(tokenized_query)

        bm25_top_indices = np.argsort(bm25_scores)[::-1][:top_k]
        bm25_results = [documents[i] for i in bm25_top_indices]

        # RRF Fusion
        fused_results = reciprocal_rank_fusion(
            [vector_results, bm25_results]
        )

        return fused_results[:top_k]

    return hybrid_search