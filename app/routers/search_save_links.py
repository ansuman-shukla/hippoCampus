# links.py - API endpoints
from fastapi import APIRouter, Depends
from app.schema.link_schema import Link as link_schema
from app.core.security import validate_supabase_token
from app.services.pinecone_service import save_to_vector_db

router = APIRouter()

@router.post("/save")
async def save_link(
    link_data: link_schema,
    user_id: str = Depends(validate_supabase_token)
):
    await save_to_vector_db(
        obj=link_data,
        namespace=user_id  # Use Supabase UUID as Pinecone namespace
    )
    return {"status": "saved"}


@router.post("/search")
async def search_links(
    query: str,
    user_id: str = Depends(validate_supabase_token)
):
    # Pinecone search logic here
    return {"results": []}