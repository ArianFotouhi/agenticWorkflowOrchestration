# LLM/pinecone_vec_store.py

import os
import time
from typing import List, Dict, Tuple
from pinecone import Pinecone


class PineconeVectorStore:
    def __init__(self,  namespace: str = "example-namespace"):
        self.namespace = namespace
        self.index_name = "index-policies"
        self.pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        self._initialize_index()
        self.index = self.pc.Index(self.index_name)
        

    def _initialize_index(self):
        if not self.pc.has_index(self.index_name):
            self.pc.create_index_for_model(
                name=self.index_name,
                cloud="aws",
                region="us-east-1",
                embed={
                    "model": "llama-text-embed-v2",
                    "field_map": {"text": "chunk_text"}
                }
            )
            print(f"✅ Created new Pinecone index '{self.index_name}'")
        else:
            print(f"ℹ️ Using existing Pinecone index '{self.index_name}'")

    def upsert_data(self,texts_with_meta: List[Dict]):
        print(f"⬆️ Upserting {len(self.texts_with_meta)} records to Pinecone...")
        self.index.upsert_records(self.namespace, self.texts_with_meta)
        time.sleep(10)
        print("✅ Upsert complete and indexed.")

    def describe_index(self) -> Dict:
        return self.index.describe_index_stats()

    def search(self, query: str, category: str, top_k: int = 3, rerank_top_n: int = 10) -> List[Tuple[str, Dict]]:
        print(f"🔍 Performing category-filtered search for: '{query}' in '{category}'")

        results = self.index.search(
            namespace=self.namespace,
            query={
                "top_k": top_k,
                "inputs": {
                    "text": query
                },
                "filter": {"category": category},

            },
            rerank={
                "model": "bge-reranker-v2-m3",
                "top_n": rerank_top_n,
                "rank_fields": ["chunk_text"]
            }
        )

        hits = results.get("result", {}).get("hits", [])
        return [
            (
                hit["fields"]["chunk_text"],
                {
                    "_id": hit["_id"],
                    "category": hit["fields"].get("category"),
                    "score": round(hit["_score"], 2)
                }
            )
            for hit in hits
        ]