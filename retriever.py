from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
import numpy as np

class QdrantRetriever:
    def __init__(self, data_file="monuments.txt"):
        self.data_file = data_file
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.client = QdrantClient(":memory:")  
        self.collection_name = "monuments"
        self.build_index()

    def build_index(self):
        with open(self.data_file, "r", encoding="utf-8") as file:
            self.documents = [line.strip() for line in file.readlines()]

        
        self.client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )

        
        for idx, doc in enumerate(self.documents):
            embedding = self.model.encode(doc).tolist()
            self.client.upsert(
                collection_name=self.collection_name,
                points=[PointStruct(id=idx, vector=embedding, payload={"text": doc})],
            )

    def retrieve(self, query, top_k=1):
        query_embedding = self.model.encode(query).tolist()
        search_result = self.client.search(
            collection_name=self.collection_name, query_vector=query_embedding, limit=top_k
        )

        return [hit.payload["text"] for hit in search_result] if search_result else ["No matching information found."]

retriever = QdrantRetriever()
