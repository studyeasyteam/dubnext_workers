from pydantic import BaseModel
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime

class Sample(BaseModel):
    document_id: Optional[UUID]
    document_name: Optional[str] = None

