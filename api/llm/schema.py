from pydantic import BaseModel, Field
from typing import List


class Item(BaseModel):
    eventName: str = Field(description="The name of the event")
    location: str = Field(default="", description="The name of the location of the event")
    opening_hours: str = Field(default="", description="The hours that the event is open in the format of HH:MM-HH:MM")
    min_cost: str = Field(default="", description="The minimum recommended cost to participate in the event")
    max_cost: str = Field(default="", description="The maximum recommended cost to participate in the event")
    sector: str = Field(default="Unknown", description="The type of activity. It must be one of the following four options: restaurant, activity, flight, hotel.")
    url: str = Field(default="", description="The url for more information about the event")
    description: str = Field(default="", description="A very short description of the event, about 30 words.")
    latitude: str = Field(default="-1", description="The latitude coordinates of the location. Must be a single floating point number.")
    longitude: str = Field(default="-1", description="The longitude coordinates of the location. Must be a single floating point number.")

class Items(BaseModel):
    projects: List[Item] = Field(description="List of items")