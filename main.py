from jose import jwt, JWTError
from fastapi import FastAPI, Request, HTTPException
import os
from dotenv import load_dotenv
from app.routers.search_save_links import router as search_save_links_router
from fastapi import Request, HTTPException
from jose import JWTError
from app.utils.jwt import decodeJWT, create_tokens
from app.services.user_service import create_user_if_not_exists



load_dotenv()
app = FastAPI() 


async def auth_middleware(request: Request):
    # Get the access token from the request
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")

    if not access_token:
        raise HTTPException(status_code=401, detail="Access token is missing")
    
    if refresh_token:
        token = await create_tokens(refresh_token)
        return token

    # Validate the access token
    try:
        payload = await decodeJWT(access_token)
        user_id = payload.get("sub")
       
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
    
    create_user_if_not_exists(payload)


    # Continue the request
    request.state.user_id = user_id

app.include_router(search_save_links_router)

@app.get("/")
async def root():
    return {"message": "Pls do /save to save a link or /search to search for a link"}