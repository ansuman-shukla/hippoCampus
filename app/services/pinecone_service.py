from app.core.pineConeDB import create_retriever
from app.schema.link_schema import Link as LinkSchema
from app.utils.site_name_extractor import extract_site_name
from langchain_core.documents import Document
from typing import List
from typing import Optional, Dict


async def save_to_vector_db(obj: LinkSchema, namespace: str):
    # Save the object to Pinecone
    retriever = create_retriever(namespace=namespace)
    site_name = await extract_site_name(obj.link)
    
    # Create metadata dictionary
    metadata = {
        "title": obj.title,
        "note": obj.note,
        "site_name": site_name
    }
    
    # Combine text content and include metadata
    text_to_save = f"{obj.title} {obj.note} {site_name}"
    await retriever.add_texts(
        texts=[text_to_save],
        metadatas=[metadata],
        namespace=namespace
    )
    return {"status": "saved"}


async def search_vector_db(
    query: str,
    namespace: str,
    filter: Optional[Dict] = None,
    top_k: int = 10
) -> List[Document]:
    
    retriever = create_retriever(namespace=namespace)
    retriever.top_k = top_k
    
    # Include metadata filter in the search
    results = retriever.get_relevant_documents(
        query,
        filter=filter  # Pass the metadata filter here
    )
    return results