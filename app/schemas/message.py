from pydantic import BaseModel
# Generic response model for returning simple messages in API responses

class Message(BaseModel):
    message: str
