from pydantic import BaseModel

class Link(BaseModel):
    title: str
    note: str
    link: str
    

class Memory_Schema(BaseModel):
    title: str
    note: str
    site_name: str
    date: str
    source_url: str
    doc_id: str