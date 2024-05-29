from typing import Dict, Any

from pydantic import BaseModel

class UserBase(BaseModel):
    username: str 

class UserCreate(UserBase):
    password_hash: str

class User(UserBase):
    id: int
    session_data: Dict[str, Any]
    role : str

    class Config:
        from_attributes = True


class FormulaBase(BaseModel):
    signal_name: str
    formula: str
    threshold: float
    invert: bool
    graph_type : str
    graph_detail: str
    widget_data: Dict[str, Any]

class Formula(FormulaBase):
    id:int
    username: str

    class Config:
        from_attributes = True


