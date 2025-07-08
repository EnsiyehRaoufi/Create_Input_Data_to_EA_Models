"""
Load entity representation vectors from JSON and print basic statistics:
first vector, its dimensionality, and total count of vectors.
"""

import json
from Param import *

# Open JSON file containing all entity vectors
with open(INPUT_DIR+DATASET+'_vectorList.json') as user_file:
  # Parse JSON into a Python list of vectors
  parsed_json = json.load(user_file)

# Display the first entity’s vector
print("First vector: ",parsed_json[0])
# Display each vector dimension
print("Vector length: ", len(parsed_json[0]))
# Display how many entity vectors were loaded
print("Number of entity vectors: ", len(parsed_json))
