# app/core/security.py

from fastapi import Request, HTTPException
from jose import jwt, JWTError
from app.core.config import settings

async def get_current_user(request: Request) -> str:
    # Get token from cookies
    access_token = request.cookies.get("access_token")
    
    if not access_token:
        raise HTTPException(status_code=401, detail="Missing access token")

    try:
        payload = jwt.decode(
            access_token,
            settings.SUPABASE_ANON_KEY,
            algorithms=["HS256"]
        )
        return payload.get("sub")  # Return only user_id
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")