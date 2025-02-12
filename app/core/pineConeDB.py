from pinecone import Pinecone
from app.core.config import settings
from langchain_community.retrievers import PineconeHybridSearchRetriever
from pinecone_text.sparse import BM25Encoder
import nltk
from pinecone import Pinecone,ServerlessSpec
from langchain_google_genai import GoogleGenerativeAIEmbeddings



index_name = settings.PINECONE_INDEX

GEMINI_API_KEY = settings.GEMINI_API_KEY

pc = Pinecone(api_key=settings.PINECONE_API_KEY)

if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=768,
        metric='dotproduct',
        spec=ServerlessSpec(cloud='aws', region='us-east-1')
    )

index = pc.Index(index_name)

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-004" , google_api_key=GEMINI_API_KEY)

bm25encoder = BM25Encoder()

def create_retriever(namespace: str):
    return PineconeHybridSearchRetriever(index=index, embeddings=embeddings, sparse_encoder=bm25encoder , namespace=namespace)


