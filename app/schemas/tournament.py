from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field,field_validator


class TournamentCreate(BaseModel):
    name: str = Field(..., max_length=100)
    max_players: int = Field(..., gt=0)
    start_at: datetime

    @field_validator('start_at')
    @classmethod
    def validate_start_at(cls, v: datetime) -> datetime:
        """Ensures datetime is timezone-naive before saving to DB."""
        return v.replace(tzinfo=None)  

class TournamentOut(BaseModel):
    id: int
    name: str
    max_players: int
    start_at: datetime
    registered_players: Optional[list] = None

    @field_validator('start_at')
    @classmethod
    def validate_start_at(cls, v: datetime) -> datetime:
        """Ensures datetime is timezone-naive before saving to DB."""
        return v.replace(tzinfo=None)  
    
    model_config = {
        "from_attributes": True,
    }


