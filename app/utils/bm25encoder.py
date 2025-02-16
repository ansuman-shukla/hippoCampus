from pymongo import MongoClient
from pinecone_text.sparse import BM25Encoder
import json
from datetime import datetime
from typing import Optional
from app.core.config import settings

# MongoDB setup
client = MongoClient(settings.MONGODB_URI)
db = client["search_system"]
bm25_collection = db["bm25_models"]

class BM25Storage:
    @staticmethod
    def save_model(encoder: BM25Encoder, namespace: str):
        """Save BM25 state to MongoDB"""
        model_data = {
            "namespace": namespace,
            "state": encoder.dump(),
            "timestamp": datetime.now()
        }
        bm25_collection.update_one(
            {"namespace": namespace},
            {"$set": model_data},
            upsert=True
        )

    @staticmethod
    def load_model(namespace: str) -> Optional[BM25Encoder]:
        """Load BM25 state from MongoDB"""
        doc = bm25_collection.find_one({"namespace": namespace})
        if not doc:
            return None
        encoder = BM25Encoder()
        return encoder