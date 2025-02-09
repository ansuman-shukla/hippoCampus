from jose import jwt, JWTError, ExpiredSignatureError
from app.core.config import settings
from fastapi import HTTPException
import httpx

def decodeJWT(access_token: str) -> dict:
    if not access_token:
        raise HTTPException(status_code=401, detail="Missing access token")

    try:
        # Decode the token with leeway for clock skew
        payload = jwt.decode(
            access_token,
            settings.SUPABASE_ANON_KEY,
            algorithms=["HS256"],
            leeway=30  # 30 seconds leeway for expiration
        )
        
        # Ensure the token includes an 'exp' claim
        if 'exp' not in payload:
            raise HTTPException(status_code=401, detail="Token has no expiration")
            
        return payload
        
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
    
async def create_tokens(refresh_token: str) -> dict:
    url = f"{settings.SUPABASE_URL}/auth/v1/token"
    headers = {
        "Authorization": f"Bearer {settings.SUPABASE_ANON_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "refresh_token": refresh_token,
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise ValueError(f"Supabase refresh failed: {e.response.text}") from e
        except httpx.RequestError as e:
            raise ConnectionError(f"Connection failed: {str(e)}") from e
        
    return None



        