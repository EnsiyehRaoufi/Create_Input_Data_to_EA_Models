# Create Input Files to the Entity Alignment Models from TTL/XML/NT Source and Target KGs

📢 **Note**: The results of this work contributed to a Semantic Web Journal submission, available here:  
[An Analysis of the Performance of Representation Learning Methods for Entity Alignment: Benchmark vs. Real-world Data](https://www.semantic-web-journal.net/content/analysis-performance-representation-learning-methods-entity-alignment-benchmark-vs-real-0)

This repository creates proper input files for various Entity Alignment (EA) models using reference alignment files and RDF-based source and target knowledge graphs in `.ttl`, `.xml`, or `.nt` formats.

Please note: the generated inputs are formatted to allow EA models to run on a wide variety of datasets without causing runtime errors, even on real-world and heterogeneous KGs.

We preprocess and generate the required JSON, PKL, and text files for original implementations of the following EA methods:
- [BERT-INT](https://github.com/kosugi11037/bert-int)
- [RDGCN](https://github.com/StephanieWyt/RDGCN)
- [MultiKE](https://github.com/nju-websoft/MultiKE)
- [i-Align](https://bitbucket.org/bayudt/i-align/src/master/)

In addition, given a source and target KG and a reference alignment file (in TTL/XML/NT formats), this repository supports preparing inputs for the [Entity-Matchers](https://github.com/epfl-dlab/entity-matchers) framework. Using Entity-Matchers, you can easily run and evaluate multiple EA models on your custom datasets.

To promote fair evaluation, we move beyond the commonly used Hits@K metric and instead report **Precision, Recall, and F1-Score**, enabling better alignment quality analysis.

> 🛠️ **Community Note**: Any contributions that add input generation scripts for other EA models are highly encouraged!

## 🎯 Purpose

Most existing EA models assume that their input files are already pre-processed and formatted according to specific internal conventions. As a result, researchers often reuse limited benchmark datasets and avoid experimenting with new or real-world KGs.

This tool removes that barrier by transforming raw input files—two KGs (in `.ttl`, `.nt`, or `.xml`) and an alignment file—into the exact format expected by each EA model, **without modifying the original EA code**. This facilitates fair comparison, reproducibility, and exploration of EA performance on arbitrary datasets.

## 🔍 Scripts Overview

### 1. `prepare_data.py`

- **Purpose**: Parses RDF knowledge graphs and a reference alignment file to generate input files required by downstream EA models.
- **Inputs**:
  - Set via `param.py`:
    - `source_file_name`, `target_file_name`, `reference_alignment_file`
    - file format (e.g., `ttl`, `xml`, `nt`)
    - EA model-specific configuration parameters
- **Outputs**: See the [📤 Output Files](#-output-files) section below.
- **Execution**:
  1. Place all raw files (`source`, `target`, and `alignment`) into the `raw_files/` directory
  2. Edit the `param.py` file to define:
     - File names (without folder prefix)
     - File types (e.g., `'ttl'`, `'xml'`)
     - Optional model-specific settings
  3. Run the script via:
     ```bash
     bash run.sh
     ```

---

## 🧭 Execution Order

1. Place your `.ttl`, `.xml`, or `.nt` files in the `raw_files/` folder
2. Edit `param.py` to set filenames and parameters
3. Run:
   ```bash
   bash run.sh
   ```

---

## 📤 Output Files

The output of this tool consists of **model-specific input files** generated from the raw KGs and alignment file. These outputs are fully compatible with the original implementations of EA models such as BERT-INT, RDGCN, MultiKE, etc.

The generated files vary depending on the selected EA model (defined in `param.py`).

### Example: BERT-INT Input Files
The following 11 files are produced when preparing Zh-En data for the BERT-INT model:

- `ent_ids_1`: Entity IDs and URIs in source KG
- `ent_ids_2`: Entity IDs and URIs in target KG
- `ref_pairs`: Test entity alignment pairs (ID-encoded)
- `sup_pairs`: Training entity alignment pairs (ID-encoded)
- `rel_ids_1`: Relation IDs and labels in source KG
- `rel_ids_2`: Relation IDs and labels in target KG
- `triples_1`: Source KG triples (ID-encoded)
- `triples_2`: Target KG triples (ID-encoded)
- `zh_att_triples`: Source KG attribute triples
- `en_att_triples`: Target KG attribute triples
- `ent_desc.pkl`: Pickled dictionary of entity descriptions

> 🧩 These are directly usable as inputs to BERT-INT without modifying its code.

### Notes
- For other models like RDGCN, the format and file names differ, and are automatically generated accordingly.
- All outputs are saved in a dedicated subfolder for each dataset/model combination.

---

## 🤝 Community Recommendation: Encourage Reproducible Input Pipelines

To promote reproducibility, adaptability, and broader adoption of EA models, we encourage researchers developing new Entity Alignment methods to **publicly share the scripts they use to convert raw RDF knowledge graphs and alignment files into the specific input format required by their models**.

Too often, EA systems are tightly coupled with benchmark-specific preprocessing pipelines, making it difficult for others to test them on new datasets. By sharing input generation code alongside model code, the EA community can:

- Enable the application of models to **real-world or domain-specific KGs**
- Simplify **benchmarking** across diverse datasets
- Support **transparent and fair comparisons**
- Encourage the **reuse of models** beyond the initial dataset they were trained on

We hope this repository serves as a practical example of how to design a modular and extensible input generation pipeline, applicable to a wide variety of EA models.
