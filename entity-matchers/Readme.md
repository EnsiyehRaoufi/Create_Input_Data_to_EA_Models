Create input files to be used in the [Entity‑Matchers](https://github.com/epfl-dlab/entity-matchers) pipeline (by having the source KG, target KG, and reference alignment files in ttl, xml or nt format). Employing Entity-Matchers you can run experiments of several entity alignment models on your dataset by reporting precision, recall, and F1-score instead of Hit@K as the evaluation metrics.

1. Please put the source KG, target KG, and reference alignment files in the "raw_files" folder. Then,
2. Please fill out the necessary parameters in the Param.py file. Then,
3. Please run the run.sh file (you can run it in the command window using: bash run.sh) 

All the input files to the Entity-matcher's models then will be created in this directory: ./Entity_Matchers_inputs/DATASET_en/
Also a Pickle dictionary for each dataset will be created in the following directory: ./Entity_Matchers_inputs/dictionaries-bert-int which you need to address these dictionaries as arguments when running BERT-INT on a dataset.

---

## ⚙️ Configuration Guide: `Param.py` for Entity-Matchers Input Generation

Before generating the input files, you must fill out `Param.py`, which defines how your RDF data is processed. Below is a full breakdown of each parameter:

### 📂 File and Format Configuration
```python
KG_FILES = ["source.ttl", "target.ttl"]
```
- Names of the RDF files for the source and target knowledge graphs.

```python
KG_FORMAT = 'ttl'
```
- Format of the KG files. Can be `'ttl'`, `'nt'`, or `'xml'`.

```python
ALIGN_FILE = "same_as.rdf"
ALIGN_FORMAT = 'xml'
```
- File name and format of the reference alignment file between the source and target entities.

```python
DATASET = 'doremus'
```
- A short, clean dataset identifier (used for folder naming). Avoid punctuation and spaces.

---

### 🗂 Folder Paths
```python
PATH = './raw_files/' + DATASET + '/'
INPUT_DIR = './Entity_Matchers_inputs/' + DATASET + '/'
```
- `PATH` is where the raw input RDF and alignment files are stored.
- `INPUT_DIR` is where the generated files will be saved. This is automatically structured using the dataset name.

---

### 🧪 Data Splitting and Validation Settings
```python
TEST_SIZE = 7  # means 70% test
VAL_SIZE = 1   # means 10% validation
NUM_FOLD = 5
```
- These control how the reference alignments are split for training, validation, and test sets (percent-based).
- `NUM_FOLD` is the number of cross-validation folds to use for training splits.

---

### 🌀 Handling Special Cases
```python
HANDL_BLANK_NODE = 1
```
- If enabled (set to `1`), this option adds useful literals of blank nodes into entity descriptions, which is particularly important for models like BERT-INT that use textual descriptions of entities.

---

With this flexible parameter setup, your pipeline can prepare standardized input formats for a wide variety of EA experiments on custom RDF datasets — without rewriting model-specific preprocessing logic.



## 📌 Summary: Comparison of our Analysis Pipeline with the Entity‑Matchers Framework

This tool complements the [Entity‑Matchers](https://github.com/epfl-dlab/entity-matchers) framework by adding a **missing capability**: converting raw RDF files (`.ttl`, `.nt`, `.xml`) and reference alignments into the standardized input format expected by their framework.

Whereas the official pipeline:
- Provides pre-formatted datasets only
- Modifies EA model code to fit its unified structure
- Focuses on classification metrics (P/R/F1)

Our contribution:
- Automatically generates Entity-Matchers-compatible input files from RDF KGs
- Keeps the original EA model code untouched
- Enables running **fair comparisons across multiple EA models** on custom datasets

This bridges the gap between reusable model evaluation and real-world KG diversity, promoting **reproducibility, fairness, and flexibility** in EA benchmarking.

