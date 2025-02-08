# links.py - API endpoints
from fastapi import APIRouter, Depends , HTTPException
from app.schema.link_schema import Link as link_schema
from app.core.security import get_current_user
from app.services.pinecone_service import save_to_vector_db , search_vector_db

router = APIRouter()

@router.post("/save")
async def save_link(
    link_data: link_schema,
    user_id: str = Depends(get_current_user)
):
    try:
        await save_to_vector_db(
            obj=link_data,
            namespace=user_id
        )
        return {"status": "saved"}
    except Exception as e:
        raise HTTPException(500, "Failed to save link")



@router.post("/search")
async def search_links(
    query: str,
    user_id: str = Depends(get_current_user)
):
    try:
        results = await search_vector_db(
            query=query,
            namespace=user_id
        )
    except Exception as e:
        raise HTTPException(500, "Failed to search links")
    # Pinecone search logic here
    return results