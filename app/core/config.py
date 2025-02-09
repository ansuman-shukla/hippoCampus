from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SUPABASE_URL: str
    SUPABASE_API_KEY: str
    SUPABASE_ANON_KEY: str
    MONGODB_DB: str
    MONGODB_URI: str
    PINECONE_API_KEY: str
    PINECONE_INDEX: str
    GEMINI_API_KEY: str
    MONGODB_COLLECTION: str


    class Config:
        env_file = ".env"

settings = Settings()