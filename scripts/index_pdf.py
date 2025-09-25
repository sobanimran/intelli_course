import os
from app.rag import load_and_index

data_folder = "data"

for file in os.listdir(data_folder):
    if file.endswith(".pdf"):
        print(f"📄 Indexing {file}...")
        load_and_index(os.path.join(data_folder, file))
