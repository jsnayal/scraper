from pydantic import BaseModel
from typing import Optional


class Settings(BaseModel):
    page_limit: int = 5
    proxy: Optional[dict] = None


class Recipient(BaseModel):
    name: str
    email: Optional[str] = ''
    contact_number: Optional[str] = ''

