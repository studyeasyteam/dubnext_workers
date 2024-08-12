# import uuid
# from typing import Optional
#
# from ..models.database import SessionLocal
# from ..models.models import Sample
# from app.schemas.model_schema import (Sample)
# import json
#
#
# def Sample(doc_schema: DocumentSchema) -> Document:
#     db = SessionLocal()
#     doc_schema.document_id = uuid.uuid4()
#     document = Document(**doc_schema.dict())
#     db.add(document)
#     db.commit()
#     db.refresh(document)
#     return document
