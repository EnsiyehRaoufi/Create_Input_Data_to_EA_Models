Create input files to the [BERT-INT](https://github.com/kosugi11037/bert-int) entity alignment model having the source KG, target KG, and reference alignment files in ttl, xml or nt format.

All the input files to the BERT-INT model then will be created in this directory: ./bert_int_inputs/DATASET_en/

---

## 🚀 How to Use This Pipeline for BERT-INT Input Preparation

This script converts your RDF-based source and target Knowledge Graphs (KGs) and alignment file into the format required by the [BERT-INT](https://github.com/kosugi11037/bert-int) model.

### 🗂 Input Preparation

- Place your source and target KGs, along with the reference alignment file, in the directory specified in `Param.py` (default is `./raw_files/`).

### ⚙️ Configuration in `Param.py`

Edit the following parameters:

```python
KG_FILES = ["source.ttl", "target.ttl"]
KG_FORMAT = 'ttl'
ALIGN_FILE = "refDHT.rdf"
ALIGN_FORMAT = 'xml'
DATASET = 'doremus'
```
- These define the names and formats of the input RDF files and the dataset name used for outputs.

```python
DICT_NAME = 'desc_doremus'
```
- The name of the output dictionary that will be used by BERT-INT.

```python
TEST_REF_SIZE = 0.7
```
- The portion of the alignment file to be reserved for testing (e.g., 0.7 = 70%).

```python
HANDL_BLANK_NODE = 1
```
- If set to `1`, the pipeline resolves blank nodes to preserve literal descriptions.  
  For instance:
  ```
  <eventX> <falls_within> _:b1 .
  _:b1 <is_identified_by> "20th century" .
  ```
  becomes:
  ```
  <eventX> <falls_within> "20th century"
  ```
  This ensures that entities receive meaningful descriptions even when blank nodes are used.

If set to `0`, all triples involving blank nodes will be discarded. This may result in a loss of descriptive literals and reduce entity informativeness — which may negatively impact alignment models that rely on rich textual inputs.

### ▶️ Running the Script

Once your parameters are set, execute the pipeline with:

```bash
bash run.sh
```

The converted files for BERT-INT will be saved under:

```
./bert_int_inputs/<DATASET>_en/
```

These include:
- entity and relation mappings
- attribute triples
- alignment splits
- textual dictionaries for entity description input to the BERT encoder

---
