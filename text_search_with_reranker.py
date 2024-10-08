# -*- coding: utf-8 -*-
"""text-search-with-reranker.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/15_iIwk8g3twUGihstbjYlv7qNj2ZkwJ5
"""

!pip install "docarray[hnswlib]" transformers torch numpy pandas

!unzip ml-latest-small.zip

import pandas as pd
from docarray import BaseDoc, DocList
from docarray.typing import NdArray
from docarray.index import HnswDocumentIndex
from transformers import AutoModelForSequenceClassification, AutoModel
import torch

# Load the MovieLens dataset
movies = pd.read_csv('ml-latest-small/movies.csv')

class MovieDoc(BaseDoc):
    title: str
    genres: str
    embedding: NdArray[768]  # Using Jina embeddings dimension

# Initialize the Jina embeddings model
embedding_model = AutoModel.from_pretrained('jinaai/jina-embeddings-v2-base-en', trust_remote_code=True)
embedding_model.to('cuda' if torch.cuda.is_available() else 'cpu')
embedding_model.eval()

# Function to compute embeddings
def compute_embedding(text):
    with torch.no_grad():
        embeddings = embedding_model.encode([text])
        return embeddings[0]  # Return the first (and only) embedding

# Generate embeddings for movie titles
movies['embedding'] = movies['title'].apply(compute_embedding)

movies

# Create and index documents
doc_index = HnswDocumentIndex[MovieDoc](work_dir='/content/data')
docs = DocList[MovieDoc](
    [MovieDoc(title=row['title'], genres=row['genres'], embedding=row['embedding']) for _, row in movies.iterrows()]
)
doc_index.index(docs)

# Initialize the reranker model
reranker_model = AutoModelForSequenceClassification.from_pretrained(
    'jinaai/jina-reranker-v2-base-multilingual',
    torch_dtype="auto",
    trust_remote_code=True
)
reranker_model.to('cuda' if torch.cuda.is_available() else 'cpu')
reranker_model.eval()

# Function to perform search and reranking
def search_and_rerank(query, limit=20):
    # Compute query embedding
    query_embedding = compute_embedding(query)

    # Initial search
    matches, scores = doc_index.find(query_embedding, search_field='embedding', limit=limit)
    initial_results = [{"title": match.title, "genres": match.genres, "score": float(score)} for match, score in zip(matches, scores)]

    # Prepare for reranking
    documents = [result['title'] for result in initial_results]
    sentence_pairs = [[query, doc] for doc in documents]

    # Rerank
    with torch.no_grad():
        rerank_scores = reranker_model.compute_score(sentence_pairs, max_length=1024)

    # Combine results with rerank scores
    reranked_results = [
        {**result, "rerank_score": float(rerank_score)}
        for result, rerank_score in zip(initial_results, rerank_scores)
    ]

    # Sort by rerank score
    reranked_results.sort(key=lambda x: x['rerank_score'], reverse=True)

    return reranked_results

# Example usage
query = "fantasy pirate adventure"
results = search_and_rerank(query)
for result in results[:10]:
    print(f"Title: {result['title']}")
    print(f"Genres: {result['genres']}")
    print(f"Initial Score: {result['score']:.4f}")
    print(f"Rerank Score: {result['rerank_score']:.4f}")
    print()

