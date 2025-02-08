from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer
from jose import JWTError, jwt
from .config import settings

security = HTTPBearer()

def validate_supabase_token(access_token) -> str:
    try:
        payload = jwt.decode(
            access_token,
            key=settings.SUPABASE_ANON_KEY,  # Supabase uses anon key as JWT secret
            algorithms=["HS256"]
        )
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id , payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")