from jose import jwt, JWTError
from fastapi import FastAPI, Request, HTTPException
import os
from dotenv import load_dotenv



load_dotenv()
app = FastAPI() 


supabase_jwt_secret = os.getenv("supaBaseJWTSecret")
if not supabase_jwt_secret:
    raise ValueError("SUPABASE_JWT_SECRET environment variable is not set")

JWT_ALGORITHM = "HS256"

@app.get("/auth")
async def auth_callback(request: Request):
    token = request.query_params.get("access_token")
    if not token:
        raise HTTPException(status_code=400, detail="No access token provided.")

    try:
        data = jwt.decode(
            token,
            supabase_jwt_secret,
            algorithms=[JWT_ALGORITHM],
            audience="authenticated", 
            options={"verify_exp": True}
        )
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Token verification failed: {str(e)}")

    # Extract data from the decoded JWT
    user_id = data.get("sub")
    email = data.get("email")
    role = data.get("role")
    created_at = data.get("created_at")
    last_sign_in_at = data.get("updated_at")  # Last sign-in is "updated_at"
    issuer = data.get("iss")  # Top-level claim

    # User metadata (e.g., name, picture)
    user_metadata = data.get("user_metadata", {})
    full_name = user_metadata.get("full_name")
    picture = user_metadata.get("picture")

    # App metadata (e.g., auth provider)
    app_metadata = data.get("app_metadata", {})
    provider = app_metadata.get("provider")
    providers = app_metadata.get("providers")

    # Combine into user_data
    user_data = {
        "user_id": user_id,
        "email": email,
        "role": role,
        "created_at": created_at,
        "last_sign_in_at": last_sign_in_at,
        "full_name": full_name,
        "picture": picture,
        "issuer": issuer,
        "sub": user_id,  # Same as "user_id"
        "provider": provider,
        "providers": providers,
    }

    return user_data