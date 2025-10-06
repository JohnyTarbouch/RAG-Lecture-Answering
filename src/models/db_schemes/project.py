from pydantic import BaseModel, Field, validator
from typing import List, Optional
from bson.objectid import ObjectId

class ProjectDBScheme(BaseModel):
    id: Optional[ObjectId] = Field(None, alias="_id")
    project_id: str = Field(..., min_length=1)
    
    @validator('project_id')
    def validate_project_id(cls, value):
        if not value.isalnum():
            raise ValueError('project_id must be alphanumeric')
        return value
    
    class Config:
        arbitrary_types_allowed = True
        
    
    @classmethod
    def get_indexes(cls) -> List[dict]:
        return [
            {
                "key": [("project_id", 1)], # Unique index on project_id
                'name': 'project_id_index',
                'unique': True
            }
        ]
 