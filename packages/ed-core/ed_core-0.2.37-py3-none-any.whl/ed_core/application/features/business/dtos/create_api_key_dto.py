from pydantic import BaseModel


class CreateApiKeyDto(BaseModel):
    name: str
    description: str
