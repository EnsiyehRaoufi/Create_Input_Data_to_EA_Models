#!/bin/sh
# Orchestrate full KG preprocessing pipeline: convert, prepare files, and vectorize names

# Convert TTL → cleaned N-Triples and generate same_as alignments
python -u ttl_to_ntriple.py
# Generate attribute/relation triples and assign entity & relation IDs
python -u create_necess_files_final.py
# Build name vectors using GloVe/BERT embeddings
python -u create_name_vectors.py
