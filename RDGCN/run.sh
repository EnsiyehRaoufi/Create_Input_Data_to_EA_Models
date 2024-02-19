#!/bin/sh
python -u ttl_to_ntriple.py
python -u create_necess_files_final.py
python -u create_name_vectors.py
