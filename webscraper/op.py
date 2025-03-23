from langchain_google_genai import ChatGoogleGenerativeAI
from browser_use import Agent, Controller
from pydantic import BaseModel

import asyncio


class event_data(BaseModel):
    description: str
    price: float
    time: str

class restaurents(BaseModel):

controller = Controller(output_model=final_data)

"""
name
location
event
hotels
restaurents
plane 

This is the trip and any requirements

find 3 events
find 3 hotels and their prices
find 3 restaurents 
find a plane ticket
"""



llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash-exp', api_key='AIzaSyDqVZJJAJ0gJ94kl2ptytUvECh1NJgT3es') 

rules = [ 
         "If you get a captcha, then don't scrape that website.",
         "If the specific query is not available, then leave the data field to its corresponding none type.",
         "through blogs or tripadvisor or google searchs and remember there descriptions",
         ]

prompt = "get the coordinates of next ai in montreal. use google maps to get the latitude and longitude"
#"This is the request: I want to go to montreal. Plan the trip, with hotel, restaurents, events and plane tickets."

async def main():
    agent = Agent(
            prompt,
            llm=llm,
            controller=controller,
        )

    result = await agent.run()
    print(final_data.model_validate_json(result.final_result()))

asyncio.run(main())
