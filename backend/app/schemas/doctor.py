from pydantic import BaseModel, ConfigDict, Field


class DoctorResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    speciality: str
    details: str
    symptoms: str
    experience: int
    location: str


class SearchResponse(BaseModel):
    results: list[DoctorResponse]
    count: int
    message: str


class ErrorResponse(BaseModel):
    error: str
    message: str


class HealthResponse(BaseModel):
    status: str = Field(examples=["healthy"])
