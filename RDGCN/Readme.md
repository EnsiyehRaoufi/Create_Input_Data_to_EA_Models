This gives you the proper input files to the [RDGCN](https://github.com/StephanieWyt/RDGCN) entity alignment model, having the xml/ttl/nt files of source and target KGs together with their reference alignment file.

The original paper used [glove.840B.300d](https://nlp.stanford.edu/projects/glove/) pre-trained English word embedding model to construct the entity names' representations. You can also use "wiki-news-300d-1M.vec" or a pre-trained BERT model such as "bert-base-multilingual-cased" for entity names' embeddings. You should download the language model in this directory and then run the code. 

Generating the Embeddings using an "Nvidia Tesla V100 SXM2 32Go" GPU takes less than 10 minutes for the large AgroLD dataset.
The proper input to the RDGCN model would be available in the 'rdgcn_inputs' folder after running the code.
You can read the JSON file that contains the entity names' representations using read_json.py

---

## 🚀 How to Use This Pipeline

To generate RDGCN-compatible inputs from your own RDF datasets:

1. **Place Input Files**  
   Put your source KG, target KG, and reference alignment files (in `.ttl`, `.nt`, or `.xml` format) into the folder defined by `PATH` in `Param.py` (default is `./raw_files/`).

2. **Configure Parameters**  
   Open `Param.py` and fill out:
   - Filenames of the KGs and alignment
   - Dataset name
   - Input and output formats
   - Pretrained embedding model (optional)

3. **Run the Conversion Script**  
   Launch the pipeline using:
   ```bash
   bash run.sh
   ```

4. **Inspect Output Files**  
   Once complete, all RDGCN input files (e.g., triples, entity and relation mappings, embedding inputs) will be available in:
   ```
   ./rdgcn_inputs/<dataset_name>_en/
   ```

---

## ⚙️ Configuration Guide: `Param.py` for RDGCN Input Generation

To generate input files compatible with the [RDGCN](https://github.com/StephanieWyt/RDGCN) model, first complete the configuration in `Param.py`. Here's an explanation of the required parameters:

### 📂 File and Format Configuration
```python
KG_FILES = ["source.nt", "target.nt"]
KG_FORMAT = 'nt'
ALIGN_FILE = "refDHT.rdf"
ALIGN_FORMAT = 'xml'
DATASET = 'doremus'
```
- `KG_FILES`: The filenames of the source and target knowledge graphs.
- `KG_FORMAT`: Format of the input RDF files. Options: `'ttl'`, `'xml'`, `'nt'`.
- `ALIGN_FILE` / `ALIGN_FORMAT`: File and format of the ground-truth alignment.
- `DATASET`: A clean identifier for the dataset (used in output path). Avoid punctuation.

### 🗂 Folder Paths
```python
PATH = './raw_files/'
INPUT_DIR = './rdgcn_inputs/' + DATASET + '_en/'
```
- `PATH`: Directory where source, target, and alignment RDF files are placed.
- `INPUT_DIR`: Output path where generated RDGCN inputs will be stored.

### 🔤 Pre-trained Word Embeddings
```python
PRETRAINED_TEXT_EMB_MODEL = 'glove.840B.300d.txt'
DIM = 300
```
- `PRETRAINED_TEXT_EMB_MODEL`: Path to the pre-trained word embedding model. Can be:
  - `"glove.840B.300d.txt"` from [Stanford NLP](https://nlp.stanford.edu/projects/glove/)
  - `"wiki-news-300d-1M.vec"` from fastText
  - `"bert-base-multilingual-cased"` (for BERT-style embeddings)
- `DIM`: Dimensionality of the entity name representations (typically 300 for glove or fastText).

---

After configuring `Param.py`, simply run the pipeline using:

```bash
bash run.sh
```

Upon completion, the formatted inputs for RDGCN will be available in the `rdgcn_inputs/` folder. You can inspect the generated entity representations using `read_json.py`.

---
