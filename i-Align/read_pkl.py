import pickle

with open('KG1_ATTRIBUTES', 'rb') as f:
    data = pickle.load(f)
print(data, len(data))
