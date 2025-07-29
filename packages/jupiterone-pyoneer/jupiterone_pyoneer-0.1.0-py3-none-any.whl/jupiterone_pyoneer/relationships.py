from pydantic import BaseModel, Field

class Relationship(BaseModel):
    key: str = Field(..., alias="_key", description="Unique key for the relationship")
    type: str = Field(..., alias="_type", description="Type of the relationship")
    class_: str = Field(..., alias="_class", description="Class of the relationship (e.g., VERB)")
    from_entity_key: str = Field(..., alias="_fromEntityKey", description="Source entity key")
    to_entity_key: str = Field(..., alias="_toEntityKey", description="Target entity key")
    # Additional arbitrary fields allowed
    class Config:
        extra = "allow"
        validate_by_name = True 