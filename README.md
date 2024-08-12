# Movie Search and Reranking

This project implements an efficient movie search and reranking system using embeddings and a neural reranker. It utilizes the MovieLens dataset and leverages advanced NLP models for improved search results.

## Features

- Efficient movie search using HNSW index
- Reranking of search results using a neural reranker
- Utilizes Jina AI embeddings and reranker models
- Optimized for both CPU and GPU environments

## Requirements

- Python 3.7+
- PyTorch
- Transformers
- DocArray
- Pandas
- NumPy

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/Balogunolalere/movie-search-reranker.git
   cd movie-search-reranker
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Download the MovieLens dataset and extract it in the project directory.


## How it Works

1. The system loads movie data and generates embeddings for each movie title.
2. It creates an HNSW index for efficient similarity search.
3. When a query is received, it computes the query embedding and performs an initial search.
4. The top results are then reranked using a neural reranker for improved accuracy.

## Performance Optimizations

- Uses GPU acceleration when available
- Employs efficient indexing for fast similarity search

## Future Improvements

- Implement batch processing for larger datasets
- Add support for multi-lingual queries
- Integrate with a web interface for easy user interaction

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
