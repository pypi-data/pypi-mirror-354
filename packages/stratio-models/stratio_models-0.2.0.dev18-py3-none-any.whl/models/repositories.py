# src/stratio/api/models/repositories.py

from pydantic import BaseModel


class Chart(BaseModel):
    # mandatory attributes
    repo_url: str
    name: str
    version: str


class UploadResult(BaseModel):
    # mandatory attributes
    failures: list[str]
    exists: list[str]
    success: list[str]


class DeleteResult(BaseModel):
    # mandatory attributes
    failures: list[str]
    success: list[str]
