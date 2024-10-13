#!/bin/sh
python -u ttl_to_ntriple.py
python -u create_necess_files.py
python -u split.py
