# 🧩 i-Align Input Preparation Guide

This toolkit helps generate the **required input files** to run the [i-Align Entity Alignment model](https://bitbucket.org/bayudt/i-align/src/master/), using source and target knowledge graphs in RDF format (`.ttl`, `.nt`, or `.xml`) along with a reference alignment file.

---

## 📁 Directory Setup

Place the following files in a designated folder (default is `raw_files/`, but this can be changed in `param.py`):

- `source.nt` or `source.ttl` or `source.xml`: **Source Knowledge Graph**
- `target.nt` or `target.ttl` or `target.xml`: **Target Knowledge Graph**
- `refDHT.rdf` or similar: **Reference Alignment File**

We have also included the original `char_vocab` from the i-Align repo in the same folder. This file is **automatically updated** then using our code to include any new characters detected in your dataset.

---

## 🛠 Configuration: Understanding `param.py`

Edit the `param.py` file to define how the data should be processed:

```python
# File names for source and target KGs
KG_FILES = ["source.nt", "target.nt"]

# Format of the RDF files (choose: 'ttl', 'nt', 'xml')
KG_FORMAT = 'nt'

# Custom dataset identifier (used in output directory naming)
DATASET = 'Doremus'

# Alignment file name (e.g., sameAs links or reference alignments)
ALIGN_FILE = "refDHT.rdf"

# Format of the alignment file (choose: 'ttl', 'nt', 'xml')
ALIGN_FORMAT = 'xml'

# Output directory — generated automatically based on dataset name
INPUT_DIR = './iAlign_inputs/' + DATASET + '/'

# Folder containing raw input files — default is './raw_files/'
# You can change this to use any folder name
PATH = './raw_files/'
```

---

## 🚀 Running the Pipeline

After editing the parameters:

1. Make sure all input files are placed in the folder you set as `PATH` (default: `raw_files/`).
2. Run the preprocessing script via:

```bash
bash run.sh
```

This will extract, tokenize, and encode your KG entities and properties into i-Align-compatible format.

---

## 📦 Output Files (in `iAlign_inputs/<dataset>/`)

After running the script, the following files will be generated:

| File Name         | Description                                         |
|------------------|-----------------------------------------------------|
| `KG1_ENTITIES`   | Entity list for source KG                          |
| `KG2_ENTITIES`   | Entity list for target KG                          |
| `KG1_ATTRIBUTES` | Attribute triples from source KG                   |
| `KG2_ATTRIBUTES` | Attribute triples from target KG                   |
| `KG1_ent_vocab`  | Entity vocabulary (char-level) for source KG       |
| `KG2_ent_vocab`  | Entity vocabulary (char-level) for target KG       |
| `char_vocab`     | Shared character vocabulary across both KGs        |
| `pred_vocab`     | Predicate vocabulary                               |
| `seed_data`      | Pickled training data pairs                        |
| `test_data`      | Pickled testing data pairs                         |

To inspect any of the `.pkl` files, you can use the utility script provided:

```bash
python read_pkl.py iAlign_inputs/Doremus/KG1_ENTITIES
```

---

## 🙌 Final Notes

- This setup ensures that **i-Align** can run on new or custom datasets without code changes.
- Contributions for expanding compatibility with other encoders or vocabularies are welcome!
