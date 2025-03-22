from pydantic import BaseModel, Field
from typing import List


class Project(BaseModel):
    projectName: str = Field(description="The name of the project")
    entityName: str = Field(description="The name of the organization that is requesting a proposal")
    url: str = Field(description="The url to the request of the proposal")
    description: str = Field(description="A short description of the proposal or project")
    publicationDate: str = Field(description="The publication date of the proposal")
    deadlineData: str = Field(description="The deadline date of the proposal")
    sector: str = Field(description="The sector of the project or proposal")

class Data(BaseModel):
    projects: List[Project] = Field(description="List of relevant projects")

