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


class DoctorSearchResponse(BaseModel):
    results: list[DoctorResponse]
    count: int = Field(ge=0)
    message: str
