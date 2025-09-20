from pydantic import BaseModel
from typing import  Optional


class ProjectDataResponse(BaseModel):
    file_id: str
    chunk_size: Optional[int] = 100
    over_lap: Optional[int] = 20
    do_reset : Optional[int] = 0
    
