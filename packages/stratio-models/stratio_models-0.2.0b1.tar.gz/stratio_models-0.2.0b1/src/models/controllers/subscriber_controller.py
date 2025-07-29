# src/models/controllers/subscriber_models.py
from typing import Optional

from pydantic import BaseModel, field_validator


class SubscriberRequest(BaseModel):
    # Required fields
    contactEmail: str
    contactName: str
    # Optional fields
    companyName: Optional[str] = ""
    contactPhone: Optional[str] = ""

    @field_validator("companyName", "contactPhone", mode="before")
    @classmethod
    def set_empty_string_if_none(cls, v):
        return v if v is not None else ""
