This gives you the proper input files to the [MultiKE](https://github.com/nju-websoft/MultiKE) entity alignment model having the xml/ttl/nt files of source and target KGs together with their reference alignment file.

The proper input to the MultiKE model would be available in 'multike_inputs' folder after running the codes.

---

## 🚀 How to Use This Pipeline for MultiKE Input Preparation

This script converts raw RDF files into the format required by the [MultiKE](https://github.com/nju-websoft/MultiKE) entity alignment model.

To use it:

- **Organize Your Data**  
  Place the source KG, target KG, and the alignment file inside the folder defined by the `PATH` parameter in `Param.py` (default: `./raw_files/`).

- **Configure Parameters in `Param.py`**  
  Open the file and specify:
  - `KG_FILES`: Filenames of source and target KG RDF files
  - `KG_FORMAT`: RDF serialization format (`ttl`, `nt`, `xml`)
  - `ALIGN_FILE` / `ALIGN_FORMAT`: Name and format of the alignment file
  - `DATASET`: Short identifier used for naming outputs
  - `KG1_ATTR_URI` / `KG2_ATTR_URI`: The URIs of the attributes used to extract local names of entities
  - `TEST`, `TRAIN`, `VAL`: Percentage split of the reference alignment into test/train/validation sets

- **Run the Script**  
  After saving your settings, start the conversion process with:
  ```bash
  bash run.sh
  ```

- **Find the Outputs**  
  Once finished, the files formatted for MultiKE will be saved in:
  ```bash
  ./multike_inputs/<dataset_name>/
  ```

These include entities, triples, and alignment splits needed by the MultiKE model.

---
