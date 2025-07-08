#!/bin/sh
# Orchestrate full KG preprocessing pipeline: TTL→NT conversion, file prep, and data splitting

# Convert TTL files to cleaned N-Triples and generate same_as alignments
python -u ttl_to_ntriple.py
# Generate attribute/relation triples and assign entity & relation IDs
python -u create_necess_files.py
# Create random train/validation/test splits from reference links
python -u split.py
