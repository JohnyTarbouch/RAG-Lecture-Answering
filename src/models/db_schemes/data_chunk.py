from pydantic import BaseModel, Field, validator
from typing import List, Optional
from bson.objectid import ObjectId

class DataChunkDBScheme(BaseModel):
    id: Optional[ObjectId] = Field(None, alias="_id")
    chunk_text: str = Field(..., min_length=1)
    chunk_metadata: dict
    chunk_order: int = Field(..., gt=0)
    chunk_project_id: ObjectId
    
    class Config:
        arbitrary_types_allowed = True
        
    @classmethod
    def get_indexes(cls) -> List[dict]:
        return [
            {
                "key": [("chunk_project_id", 1)], # Unique index on project_id
                'name': 'chunk_project_id_index',
                'unique': False
            }
        ]
 