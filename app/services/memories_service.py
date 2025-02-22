from app.core.database import collection_memories
from app.schema.link_schema import Memory_Schema
import logging
from typing import Dict, Any
from bson.errors import InvalidId 
from bson import ObjectId  # Changed this line
from pymongo.errors import PyMongoError
from app.exceptions.databaseExceptions import *

logger = logging.getLogger(__name__)

async def save_memory_to_db(memory_data: Memory_Schema):

    try:
    # Validate memory data
        if not memory_data:
            raise MemoryValidationError("Memory data cannot be empty")

        
        # Additional validation checks
        if not memory_data.get("title"):
            raise MemoryValidationError("Memory must have a title")
    
        # Save to database
        result = collection_memories.insert_one(memory_data)
        
        if not result.inserted_id:
            raise MemoryDatabaseError("Failed to save memory")

        # Fixed ObjectId usage
        memory_data["_id"] = str(result.inserted_id)
        logger.info(f"Successfully saved memory with id {result.inserted_id}")
        
        return {"status": "saved", "memory": memory_data}

    except PyMongoError as e:
        logger.error(f"Database error: {str(e)}")
        raise MemoryDatabaseError(f"Database error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise MemoryServiceError(f"Error saving memory: {str(e)}")

