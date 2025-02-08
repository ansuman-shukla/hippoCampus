from fastapi import APIRouter, Request, Response
from app.core.security import validate_supabase_token
from app.services.user_service import create_user_if_not_exists

router = APIRouter()

@router.post("/login")
async def login(
    request: Request,
    response: Response
):
    # Get tokens from request body
    data = await request.json()
    access_token = data.get("access_token")
    refresh_token = data.get("refresh_token")

    # Validate access token
    user_id = await validate_supabase_token(access_token)
    
    # Create user and store refresh token
    await create_user_if_not_exists(user_id, refresh_token)
    
    # Set cookies
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)
    
    return {"status": "authenticated", "user_id": user_id}