"""
Utility to load and inspect a pickle file: prints its contents and the number of items.
Usage: python read_pkl.py <pickle_file_path>
"""
import pickle

# Open the specified pickle file in binary read mode
with open('KG1_ATTRIBUTES', 'rb') as f:
    # Deserialize the pickle into a Python object
    data = pickle.load(f)
    
# Display the loaded data and the total number of items
print(data, len(data))
