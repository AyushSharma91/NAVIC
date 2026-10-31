import os

# project root path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# raw and processed data paths
DATA_DIR = os.path.join(BASE_DIR, "data")
DATA_RAW_DIR = os.path.join(DATA_DIR, "raw")
DATA_PROCESSED_DIR = os.path.join(DATA_DIR, "processed")

# output folders for maps, plots and saved model
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
MAPS_DIR = os.path.join(OUTPUT_DIR, "maps")
GRAPHS_DIR = os.path.join(OUTPUT_DIR, "graphs")
MODELS_DIR = os.path.join(OUTPUT_DIR, "models")

# default filenames
ROUTE_DATA_FILE = "route_data.csv"
SATELLITE_DATA_FILE = "satellite_data.csv"
MODEL_FILE = "random_forest.pkl"
LOG_EXTENSION = ".txt"

# make sure all directories exist
required_folders = [
    DATA_RAW_DIR,
    DATA_PROCESSED_DIR,
    OUTPUT_DIR,
    MAPS_DIR,
    GRAPHS_DIR,
    MODELS_DIR
]

for folder in required_folders:
    os.makedirs(folder, exist_ok=True)