from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class FAISSRetriever:
    def __init__(self, data_file="D:/hf/llama2/monuments.txt"):
        self.data_file = data_file
        self.model = SentenceTransformer("all-MiniLM-L6-v2")  
        self.index, self.documents = self.build_index()

    def build_index(self):
        try:
            with open(self.data_file, "r", encoding="utf-8") as file:
                self.documents = [line.strip() for line in file.readlines()]
            
            if not self.documents:
                raise ValueError("Error: The data file is empty!")

            
            embeddings = self.model.encode(self.documents, convert_to_numpy=True)

            
            dimension = embeddings.shape[1]
            index = faiss.IndexFlatL2(dimension)
            index.add(embeddings)

            return index, self.documents

        except FileNotFoundError:
            print(f"Error: {self.data_file} not found.")
            return None, []

    def retrieve(self, query, top_k=1):
        query_embedding = self.model.encode([query], convert_to_numpy=True)
        distances, indices = self.index.search(query_embedding, top_k)

        results = [self.documents[idx] for idx in indices[0] if idx < len(self.documents)]
        return results if results else ["I couldn't find any information on that."]

retriever = FAISSRetriever()
