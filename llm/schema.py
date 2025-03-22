from pydantic import BaseModel, Field
from typing import List


class Project(BaseModel):
    projectName: str = Field(description="The name of the project")
    entityName: str = Field(description="The name of the organization that is requesting a proposal")
    url: str = Field(default="", description="The URL to the request of the proposal")
    description: str = Field(default="", description="A short description of the proposal or project")
    publicationDate: str = Field(default="", description="The publication date of the proposal")
    deadlineDate: str = Field(default="", description="The deadline date of the proposal")
    sector: str = Field(default="Unknown", description="The sector of the project or proposal")

class Data(BaseModel):
    projects: List[Project] = Field(description="List of relevant projects")

