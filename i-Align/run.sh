#!/bin/sh
# Orchestrate full KG preprocessing pipeline: TTL→NT conversion, file prep, and IALIGN pickle creation

# Convert Turtle RDF to N-Triples, filter blank-node triples, and generate same_as alignments
python -u ttl_to_ntriple.py
# Generate attribute/relation triples and assign unique IDs to entities & predicates
python -u create_necess_files.py
# Build IALIGN pickle files: predicate IDs, vocabularies, seed/test splits, and feature dicts
python -u ialign_creat_pickle_files.py
