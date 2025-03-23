import json
from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, Controller
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

GEMINI_API_KEY_1 = os.environ.get("GEMINI_API_KEY_1")
GEMINI_API_KEY_2 = os.environ.get("GEMINI_API_KEY_2")
GEMINI_API_KEY_3 = os.environ.get("GEMINI_API_KEY_3")
GEMINI_API_KEY_4 = os.environ.get("GEMINI_API_KEY_4")

# Models now only contain a raw_info field to store the large block of text
class EventData(BaseModel):
    raw_info: str  # Block of text for events
    url: str
    address: str

class HotelData(BaseModel):
    raw_info: str  # Block of text for hotels
    url: str
    address: str

class RestaurantData(BaseModel):
    raw_info: str  # Block of text for restaurants
    url: str
    address: str

class FlightData(BaseModel):
    raw_info: str  # Block of text for flights
    url: str
    departure_location: str = Field("The city name of the departure location of the flight.")

class FinalData(BaseModel):
    events: list[EventData]
    hotels: list[HotelData]
    restaurants: list[RestaurantData]
    flights: list[FlightData]

# Initialize the Controller and output model
controller = Controller(output_model=FinalData)

# LLM setup for Google Gemini API
llm1 = ChatGoogleGenerativeAI(model='gemini-2.0-flash-001', api_key=GEMINI_API_KEY_1)
llm2 = ChatGoogleGenerativeAI(model='gemini-2.0-flash-001', api_key=GEMINI_API_KEY_2)
llm3 = ChatGoogleGenerativeAI(model='gemini-2.0-flash-001', api_key=GEMINI_API_KEY_3)
llm4 = ChatGoogleGenerativeAI(model='gemini-2.0-flash-001', api_key=GEMINI_API_KEY_4)

# Rules for scraping and collecting the data
rules = [
    "If you get a captcha, then don't scrape that website.",
    "If the specific query is not available, then leave the data field to its corresponding none type.",
    "Through blogs, TripAdvisor, or Google searches, and remember their descriptions.",
    "Output VALID JSON DATA ONLY PLEASE OH MY GOD DO NOT HAVE JSON AT THE BEGINNING, THE FIRST CHARACTER MUST BE { YOU STUPID GEMINI!!!",
    "The number of events specified is the MINIMUM requirement. You may exceed it, but once you meet the requirement, DO NOT scrape any new pages. Only scrape anything left on the page."
]
rules = " ".join(rules)

async def fetch_data_for_category_1(category: str, prompt: str):
    # Adjust the prompt for each category (hotels, events, restaurants, flights)
    agent = Agent(
        prompt,
        llm=llm1,
        controller=controller,
        max_failures=2,
        retry_delay=10
    )
    result = await agent.run()
    final_result = result.final_result()

    return final_result
async def fetch_data_for_category_2(category: str, prompt: str):
    # Adjust the prompt for each category (hotels, events, restaurants, flights)
    agent = Agent(
        prompt,
        llm=llm2,
        controller=controller,
        max_failures=2,
        retry_delay=10,
    )
    result = await agent.run()
    final_result = result.final_result()

    # print(final_result)

    return final_result
async def fetch_data_for_category_3(category: str, prompt: str):
    # Adjust the prompt for each category (hotels, events, restaurants, flights)
    agent = Agent(
        prompt,
        llm=llm3,
        controller=controller,
        max_failures=2,
        retry_delay=10
    )
    result = await agent.run()
    final_result = result.final_result()

    # print(final_result)

    return final_result
async def fetch_data_for_category_4(category: str, prompt: str):
    # Adjust the prompt for each category (hotels, events, restaurants, flights)
    agent = Agent(
        prompt,
        llm=llm4,
        controller=controller,
        max_failures=2,
        retry_delay=10
    )
    result = await agent.run()
    final_result = result.final_result()

    # print(final_result)

    return final_result

async def main(location, curr_location):
    # Create separate prompts for each category
    event_prompt = f"Find 2 events in {location} with description, hours open, location, and price range." + rules
    hotel_prompt = f"Find 2 hotels in {location} with description, location, price per night, and address." + rules
    restaurant_prompt = f"Find 2 restaurants in {location} with description, price range, location, and hours open." + rules
    flight_prompt = f"Find 1 flight from your city to {location} from {curr_location} with airline, price, departure/arrival time, and URL." + rules

    # Run tasks concurrently for each category
    events_task = asyncio.create_task(fetch_data_for_category_1('events', event_prompt))
    hotels_task = asyncio.create_task(fetch_data_for_category_2('hotels', hotel_prompt))
    restaurants_task = asyncio.create_task(fetch_data_for_category_3('restaurants', restaurant_prompt))
    flights_task = asyncio.create_task(fetch_data_for_category_4('flights', flight_prompt))

    # Wait for all tasks to complete
    await asyncio.gather(events_task
                         , hotels_task, restaurants_task, flights_task
                         )

    # Gather results
    events = events_task.result()
    hotels = hotels_task.result()
    restaurants = restaurants_task.result()
    flights = flights_task.result()

    res = [events, hotels, restaurants, flights]

    # Print the raw results
    print(
        res
    )

    return res

# Run the async main function
# asyncio.run(main("Toronto", "Montreal"))