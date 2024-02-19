#!/bin/sh
python -u ttl_to_ntriple.py
python -u create_necess_files.py
python -u Multike_create_local_names.py
python -u Multike_test_train_val.py
