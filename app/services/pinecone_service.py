from app.core.pineConeDB import create_retriever
from app.schema.link_schema import Link as LinkSchema
from app.utils.site_name_extractor import extract_site_name
from langchain_core.documents import Document
from typing import List
from typing import Optional, Dict
from app.exceptions.httpExceptionsSearch import *
from app.exceptions.httpExceptionsSave import *
from datetime import datetime
from app.exceptions.httpExceptionsSearch import *
from app.services.memories_service import save_memory_to_db 


async def save_to_vector_db(obj: LinkSchema, namespace: str):
    """Save document to vector database with enhanced error handling"""

    doc_id = f"{namespace}-{datetime.now().timestamp()}"

    logger_context = {
        "user_id": namespace,
        "doc_id": doc_id,
        "url": obj.link
    }
    
    try:
        logger.info("Creating vector DB retriever", extra=logger_context)
        retriever = await create_retriever(namespace=namespace)
        
        logger.info("Extracting site name", extra=logger_context)
        site_name = await extract_site_name(obj.link)
        if not site_name:
            logger.warning("Failed to extract site name", extra=logger_context)
            site_name = "Unknown Site"

        metadata = {
            "user_id": namespace,
            "title": obj.title,
            "note": obj.note,
            "source_url": obj.link,
            "site_name": site_name,
            "date": datetime.now().isoformat(),
        }
        
        #save the memories to the database
        await save_memory_to_db(metadata)

        
        text_to_save = f"{obj.title}, {obj.note} , {site_name}"
        logger.debug("Prepared document metadata", extra={**logger_context, "metadata": metadata})

        logger.info("Storing document in vector DB", extra=logger_context)
        retriever.add_texts(
            ids=[doc_id],
            texts=[text_to_save],
            metadatas=[metadata],
            namespace=namespace
        )
        
        logger.info("Document successfully stored", extra=logger_context)
        return {"status": "saved", "doc_id": doc_id}

    except VectorDBConnectionError as e:
        logger.error("Vector DB connection failed", extra=logger_context, exc_info=True)
        raise DocumentStorageError(
            message="Failed to connect to document storage",
            user_id=namespace,
            doc_id=doc_id
        ) from e
        
    except Exception as e:
        logger.error("Unexpected error during document save", extra=logger_context, exc_info=True)
        raise DocumentStorageError(
            message="Failed to save document",
            user_id=namespace,
            doc_id=doc_id
        ) from e

async def search_vector_db(
    query: str,
    namespace: Optional[str],
    filter: Optional[Dict] = None,
    top_k: int = 2
) -> List[Document]:
    """Business logic for document search"""
    # Validate inputs
    if not namespace:
        raise InvalidRequestError("Missing user uuid - please login")
    
    if not query or len(query.strip()) < 3:
        raise InvalidRequestError("Search query must be at least 3 characters")

    try:
        # Initialize retriever with proper error handling
        retriever = await create_retriever(namespace=namespace , top_k=top_k)

    except ValueError as e:
        if "Namespace not found" in str(e):
            raise MissingNamespaceError("User storage not initialized - please add documents first")
        raise VectorDBConnectionError("Failed to connect to document storage")
    
    except Exception as e:
        raise VectorDBConnectionError(f"Database connection error: {str(e)}")

    # Execute search with proper error wrapping
    try:
        results = await retriever.ainvoke(
            query,
            config={"metadata": {"filter": filter}} if filter else None,
        )
    except Exception as e:
        raise SearchExecutionError(f"Search failed: {str(e)}")


    # Post-process results
    if not results:
        raise SearchExecutionError("No documents found matching query")
    
    # Limit results to requested count
    return results
