# Source and Target KG file names (placed in the input folder)
KG_FILES = ["source.nt", "target.nt"]  # Filenames for source and target KGs

# Format of the KG files: choose one of 'nt', 'ttl', or 'xml'
KG_FORMAT = 'nt'

# Dataset name (used to name output folders and files)
# ⚠️ Avoid special characters or spaces
DATASET = 'Doremus'

# File name of the reference alignment (sameAs links)
ALIGN_FILE = "refDHT.rdf"

# Format of the reference alignment file: choose one of 'nt', 'ttl', or 'xml'
ALIGN_FORMAT = 'xml'

# Output directory for generated i-Align input files (auto-computed)
INPUT_DIR = './iAlign_inputs/' + DATASET + '/'  # No need to manually edit this

# Path to the folder containing your RDF and alignment files
# 📁 Default is './raw_files/', but you may set it to any folder you prefer
PATH = './raw_files/'
