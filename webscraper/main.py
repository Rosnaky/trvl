from firecrawl import FirecrawlApp
from pydantic import BaseModel, Field


# json schema for location
class ExtractSchema(BaseModel):
    Name: str
    Location: str
    description: str
    time: int
    price: float


app = FirecrawlApp(api_key='fc-4869bb8699bd48848dcf053b61d8da98')


data = app.scrape_url(
        'https://www.tripadvisor.ca/Attractions-g155032-Activities-c42-Montreal_Quebec.html',
        { 
         'formats': ['json'],
         'jsonOptions': {
            'schema': ExtractSchema.model_json_schema(),
          }
        }
    )
print(data)
print(data['json'])
