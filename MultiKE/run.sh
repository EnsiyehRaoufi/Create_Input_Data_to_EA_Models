#!/bin/sh
# Orchestrate full KG preprocessing pipeline: conversion, file generation, naming, and splits

# Convert TTL to N-Triples, filter blank nodes, and generate same_as alignments
python -u ttl_to_ntriple.py
# Generate attribute/relation triples, assign entity & relation IDs, and build reference alignment files
python -u create_necess_files.py
# Create human-readable local names and ID maps for predicates and entities
python -u Multike_create_local_names.py
# Split reference alignment links into train/test/validation subsets based on percentage parameters
python -u Multike_test_train_val.py
