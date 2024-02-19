import json
from Param import *

with open(INPUT_DIR+DATASET+'_vectorList.json') as user_file:
  parsed_json = json.load(user_file)

print("First vector: ",parsed_json[0])
print("Vector length: ", len(parsed_json[0]))
print("Number of entity vectors: ", len(parsed_json))
