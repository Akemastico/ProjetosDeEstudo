from ninja import Schema 
from typing import List

class TaskIn(Schema):
    name: str
    description:str | None
    developerId: int
    categories: List[int]
    
    
