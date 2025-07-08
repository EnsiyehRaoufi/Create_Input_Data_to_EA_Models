#!/bin/sh

# run.sh — orchestrate the full KG preprocessing pipeline
# Usage: bash run.sh
#   1) Convert TTL → cleaned N-Triples
#   2) Generate all downstream attribute/relation/ID files

# Step 1: parse Turtle files, filter blank-nodes, and build same_as alignments
python -u ttl_to_ntriple.py

# Step 2: split triples, assign IDs, build reference/train/test sets, and prepare BERT-INT inputs
python -u create_necess_files_final.py
