# src/models/controllers/cluster_models.py
from typing import Optional

from pydantic import BaseModel, field_validator

from models.globals import (
    ClusterSizeEnum,
)


class ClusterCreateRequest(BaseModel):
    # Required fields
    adminEmail: str
    adminUsername: str
    installationClusterSize: Optional[ClusterSizeEnum]
    installationRegion: Optional[str]
    clusterName: str
    bucketAccessKey: str
    bucketSecretKey: str
    # Optional fields
    description: Optional[str] = None

    @field_validator("description", mode="before")
    @classmethod
    def set_empty_string_if_none(cls, v):
        return v if v is not None else ""


class ClusterUpdateRequest(BaseModel):
    # Required fields
    clusterName: str
    # Optional fields
    description: Optional[str] = None

    @field_validator("description", mode="before")
    @classmethod
    def set_empty_string_if_none(cls, v):
        return v if v is not None else ""
