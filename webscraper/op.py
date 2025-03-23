from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, Controller
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

class EventData(BaseModel):
    description: str
    price: float
    time: str
    latitude: float
    longitude: float

class HotelData(BaseModel):
    name: str
    price_per_night: float
    location: str
    description: str

class RestaurantData(BaseModel):
    name: str
    price_range: str
    location: str
    description: str

class FlightData(BaseModel):
    airline: str
    price: float
    departure_time: str
    arrival_time: str

class FinalData(BaseModel):
    events: list[EventData]
    hotels: list[HotelData]
    restaurants: list[RestaurantData]
    flight: FlightData

# Initialize the Controller and output model
controller = Controller(output_model=FinalData)

# LLM setup for Google Gemini API
llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key=GEMINI_API_KEY)

# Rules for scraping and collecting the data
rules = [
    "If you get a captcha, then don't scrape that website.",
    "If the specific query is not available, then leave the data field to its corresponding none type.",
    "Through blogs, TripAdvisor, or Google searches, and remember their descriptions.",
]

prompt = """
This is the request: I want to go to Montreal. Plan the trip, with hotels, restaurants, events, and plane tickets.
Find 3 events.
Find 3 hotels with their prices.
Find 3 restaurants.
Find a plane ticket.
"""

async def main():
    agent = Agent(
        prompt,
        llm=llm,
        controller=controller,
    )

    result = await agent.run()
    # Ensure final result is in the correct format, if `final_result` is a method, use it to extract the data
    print(FinalData.model_validate_json(result.final_result()))  # validate and output the final result

# Run the async main function
asyncio.run(main())
