from ninja import Schema 
from typing import List

class TaskIn(Schema):
    title: str
    description:str | None
    categories: List[int]
    
    
