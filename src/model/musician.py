from pydantic import BaseModel


class Musician(BaseModel):
    name: str = None
    surname: str = None
    age: int = None
    instrument: str = None
