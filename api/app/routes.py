import asyncio
from flask import Blueprint, request, jsonify
from app import db
from app.models import Itinerary, TripRequest
import random
import string
import os
from dotenv import load_dotenv
from datetime import datetime
import cohere
import googlemaps
import json
from webscraper import op

from llm.llm import CohereAPI

# blueprint for streams
api_bp = Blueprint('api', __name__, url_prefix='/api')

load_dotenv()

COHERE_API_KEY = os.environ.get("COHERE_API_KEY")
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
GOOGLEMAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")

cohere_model = CohereAPI(cohere_api_key=COHERE_API_KEY, pinecone_api_key=PINECONE_API_KEY)

dummy_attractions = [
    {
        "description": "Embark on a guided hike through the lush trails of Hampstead Heath, offering breathtaking views of the city skyline and the iconic London Eye.",
        "eventName": "Hampstead Heath Hiking Tour",
        "latitude": "51.509865",
        "location": "Hampstead Heath, London, UK",
        "longitude": "-0.118092",
        "max_cost": "30",
        "min_cost": "20",
        "opening_hours": "08:00-18:00",
        "sector": "activity",
        "url": ""
    },
    {
        "description": "Indulge in a gourmet dining experience at a Michelin-starred restaurant in Soho, featuring modern British cuisine and an extensive wine list.",
        "eventName": "Dinner at Restaurant Story",
        "latitude": "51.5085",
        "location": "Soho, London, UK",
        "longitude": "-0.1257",
        "max_cost": "200",
        "min_cost": "150",
        "opening_hours": "18:00-22:00",
        "sector": "restaurant",
        "url": ""
    },
    {
        "description": "Experience the thrill of indoor skydiving in a vertical wind tunnel, simulating the sensation of freefall in a safe and controlled environment.",
        "eventName": "Indoor Skydiving at iFLY London",
        "latitude": "51.5085",
        "location": "iFLY London, London, UK",
        "longitude": "-0.1257",
        "max_cost": "80",
        "min_cost": "50",
        "opening_hours": "10:00-20:00",
        "sector": "activity",
        "url": ""
    },
    {
        "description": "Relax in a luxurious 5-star hotel in the heart of Mayfair, offering elegant rooms, a spa, and exceptional dining options.",
        "eventName": "Stay at The Ritz London",
        "latitude": "51.509865",
        "location": "Mayfair, London, UK",
        "longitude": "-0.118092",
        "max_cost": "1000",
        "min_cost": "600",
        "opening_hours": "24/7",
        "sector": "hotel",
        "url": ""
    },
    {
        "description": "Take a scenic flight over London's iconic landmarks, including the Tower Bridge, Big Ben, and the Shard, with a knowledgeable pilot providing commentary.",
        "eventName": "London Helicopter Tour",
        "latitude": "51.5085",
        "location": "London Heliport, London, UK",
        "longitude": "-0.1257",
        "max_cost": "250",
        "min_cost": "180",
        "opening_hours": "09:00-17:00",
        "sector": "activity",
        "url": ""
    },
    {
        "description": "Dine at a trendy restaurant in Shoreditch, specializing in innovative fusion cuisine and offering a unique tasting menu.",
        "eventName": "Dinner at Dishoom",
        "latitude": "51.509865",
        "location": "Shoreditch, London, UK",
        "longitude": "-0.118092",
        "max_cost": "80",
        "min_cost": "50",
        "opening_hours": "17:00-23:00",
        "sector": "restaurant",
        "url": ""
    },
    {
        "description": "Explore the historic Tower of London, home to the Crown Jewels and centuries of rich history, with a guided tour.",
        "eventName": "Tower of London Tour",
        "latitude": "51.5085",
        "location": "Tower of London, London, UK",
        "longitude": "-0.1257",
        "max_cost": "50",
        "min_cost": "30",
        "opening_hours": "09:00-17:30",
        "sector": "activity",
        "url": ""
    },
    {
        "description": "Stay in a stylish boutique hotel in the vibrant neighborhood of Camden, offering modern amenities and easy access to local attractions.",
        "eventName": "Stay at The Z Hotel Camden",
        "latitude": "51.509865",
        "location": "Camden, London, UK",
        "longitude": "-0.118092",
        "max_cost": "200",
        "min_cost": "120",
        "opening_hours": "24/7",
        "sector": "hotel",
        "url": ""
    },
    {
        "description": "Take a guided bike tour through London's iconic landmarks, including Buckingham Palace, Hyde Park, and the Houses of Parliament.",
        "eventName": "London Bike Tour",
        "latitude": "51.5085",
        "location": "London Bike Tour Meeting Point, London, UK",
        "longitude": "-0.1257",
        "max_cost": "40",
        "min_cost": "30",
        "opening_hours": "10:00-16:00",
        "sector": "activity",
        "url": ""
    },
    {
        "description": "Dine at a traditional British pub in Covent Garden, serving classic dishes and a wide selection of local beers.",
        "eventName": "Dinner at The Lamb & Flag",
        "latitude": "51.509865",
        "location": "Covent Garden, London, UK",
        "longitude": "-0.118092",
        "max_cost": "40",
        "min_cost": "25",
        "opening_hours": "12:00-22:00",
        "sector": "restaurant",
        "url": ""
    }
]

output_format = {
  "itinerary": [
    [
      {
        "description": "",
        "eventName": "",
        "latitude": "",
        "location": "",
        "longitude": "",
        "max_cost": "",
        "min_cost": "",
        "opening_hours": "hh:mm-hh:mm",
        "sector": "restaurant | activity | flight | hotel",
        "url": ""
      },
      {
        "description": "",
        "eventName": "",
        "latitude": "",
        "location": "",
        "longitude": "",
        "max_cost": "",
        "min_cost": "",
        "opening_hours": "hh:mm-hh:mm",
        "sector": "restaurant | activity | flight | hotel",
        "url": ""
      }
    ],
    [
      {
        "description": "",
        "eventName": "",
        "latitude": "",
        "location": "",
        "longitude": "",
        "max_cost": "",
        "min_cost": "",
        "opening_hours": "hh:mm-hh:mm",
        "sector": "restaurant | activity | flight | hotel",
        "url": ""
      },
      {
        "description": "",
        "eventName": "",
        "latitude": "",
        "location": "",
        "longitude": "",
        "max_cost": "",
        "min_cost": "",
        "opening_hours": "hh:mm-hh:mm",
        "sector": "restaurant | activity | flight | hotel",
        "url": ""
      }
    ]
  ]
}

asdresponse = {
  "itinerary": [
    {
      "date": "12312021",
      "activities": [
        {"eventName": "CN Tower EdgeWalk", "cost": 195, "sector": "activity"},
        {"eventName": "Gourmet Dinner Night", "cost": 50, "sector": "restaurant"},
        {"eventName": "7 West Cafe", "cost": 30, "sector": "restaurant"}
      ]
    },
    {
      "date": "01012022",
      "activities": [
        {"eventName": "Family Fun Day at the Park", "cost": 20, "sector": "activity"},
        {"eventName": "Gourmet Dinner Night", "cost": 50, "sector": "restaurant"},
        {"eventName": "7 West Cafe", "cost": 30, "sector": "restaurant"}
      ]
    },
    {
      "date": "01022022",
      "activities": [
        {"eventName": "Annual Tech Conference", "cost": 100, "sector": "activity"},
        {"eventName": "Gourmet Dinner Night", "cost": 50, "sector": "restaurant"},
        {"eventName": "7 West Cafe", "cost": 30, "sector": "restaurant"}
      ]
    },
    {
      "date": "01032022",
      "activities": [
        {"eventName": "Blind Hockey Tournament", "cost": 0, "sector": "activity"},
        {"eventName": "Gourmet Dinner Night", "cost": 50, "sector": "restaurant"},
        {"eventName": "7 West Cafe", "cost": 30, "sector": "restaurant"}
      ]
    },
    {
      "date": "01042022",
      "activities": [
        {"eventName": "NUEVOS CAMINOS", "cost": 0, "sector": "activity"},
        {"eventName": "Gourmet Dinner Night", "cost": 50, "sector": "restaurant"},
        {"eventName": "7 West Cafe", "cost": 30, "sector": "restaurant"}
      ]
    },
    {
      "date": "01052022",
      "activities": [
        {"eventName": "Wyrdo Carnival", "cost": 0, "sector": "activity"},
        {"eventName": "Gourmet Dinner Night", "cost": 50, "sector": "restaurant"},
        {"eventName": "7 West Cafe", "cost": 30, "sector": "restaurant"}
      ]
    },
    {
      "date": "01062022",
      "activities": [
        {"eventName": "CN Tower EdgeWalk", "cost": 195, "sector": "activity"},
        {"eventName": "Gourmet Dinner Night", "cost": 50, "sector": "restaurant"},
        {"eventName": "7 West Cafe", "cost": 30, "sector": "restaurant"}
      ]
    },
    {
      "date": "01072022",
      "activities": [
        {"eventName": "Family Fun Day at the Park", "cost": 20, "sector": "activity"},
        {"eventName": "Gourmet Dinner Night", "cost": 50, "sector": "restaurant"},
        {"eventName": "7 West Cafe", "cost": 30, "sector": "restaurant"}
      ]
    },
    {
      "date": "01082022",
      "activities": [
        {"eventName": "Annual Tech Conference", "cost": 100, "sector": "activity"},
        {"eventName": "Gourmet Dinner Night", "cost": 50, "sector": "restaurant"},
        {"eventName": "7 West Cafe", "cost": 30, "sector": "restaurant"}
      ]
    },
    {
      "date": "01092022",
      "activities": [
        {"eventName": "Blind Hockey Tournament", "cost": 0, "sector": "activity"},
        {"eventName": "Gourmet Dinner Night", "cost": 50, "sector": "restaurant"},
        {"eventName": "7 West Cafe", "cost": 30, "sector": "restaurant"}
      ]
    }
  ]
}

def generate_short_URL(length=8):
    characters = string.ascii_uppercase + string.digits

    while True:
        random_string = ''.join(random.choice(characters) for _ in range(length))
        if not Itinerary.query.filter_by(short_URL=random_string).first():
            return random_string
        
def generate_short_ID(length=8):
    characters = string.ascii_uppercase + string.digits

    while True:
        random_string = ''.join(random.choice(characters) for _ in range(length))
        if not TripRequest.query.filter_by(short_ID=random_string).first():
            return random_string

# route to create new stream
@api_bp.route('/generate-trip', methods=['POST'])
def generate_trip():
    # get the request data
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No input data provided'}), 400
    
    required_params = ['city', 'start_date', 'end_date', 'min_budget', 'max_budget', 'curr_location']

    for param in required_params:
        if param not in data:
            return jsonify({'error': f'Missing required parameter: {param}'}), 400

    new_trip_request = TripRequest(
        short_ID=generate_short_ID(),
        data=data
    )
    db.session.add(new_trip_request)

    trip_data = asyncio.run(op.main(data["city"], data["curr_location"]))
    print(trip_data)

    # return jsonify(trip_data), 201

    parsed_data = [json.loads(item) for item in trip_data]

    # Initialize empty lists
    events = []
    hotels = []
    restaurants = []
    flights = []

    # Extract data
    for entry in parsed_data:
        events.extend(entry.get("events", []))
        hotels.extend(entry.get("hotels", []))
        restaurants.extend(entry.get("restaurants", []))
        flights.extend(entry.get("flights", []))

    for event in events:
        try: 
            text = event["raw_info"] + f"latitude:  longitude:  eventUrl: {event["url"]}"
            cohere_model.add_document(data=text)
            # print(f"  - {event['raw_info']} (Location: {event['address']}) | {event['url']}")
        except:
            pass

    for hotel in hotels:
        try:
            text = hotel["raw_info"] + f"latitude:  longitude:  hotelUrl: {hotel["url"]}"
            cohere_model.add_document(data=text)

            # print(f"  - {hotel['raw_info']} (Location: {hotel['address']}) | {hotel['url']}")
        except:
            pass

    for restaurant in restaurants:
        try:
            text = restaurant["raw_info"] + f"latitude:  longitude:  restaurantUrl: {restaurant["url"]}"
            cohere_model.add_document(data=text)

            # print(f"  - {restaurant['raw_info']} (Location: {restaurant['address']}) | {restaurant['url']}")
        except:
            pass

    for flight in flights:
        try:
            text = restaurant["raw_info"] + f"departure_location:  longitude:  restaurantUrl: {restaurant["url"]}"
            cohere_model.add_document(data=text)
            
            # print(f"  - {flight['raw_info']} (Departure: {flight.get('departure_location', 'Unknown')}) | {flight['url']}")
        except:
            pass

    # find num_docs by calculating substrings of data['start_date'] and data['end_date'], num_docs = num_days * 10
    start_date = datetime.strptime(data['start_date'], '%m%d%Y')
    end_date = datetime.strptime(data['end_date'], '%m%d%Y')

    # Calculate the difference in days
    num_days = (end_date - start_date).days

    num_docs = num_days * 2

    ### ADDRESS TO LATITUDE AND LONGITUDE
    # Initialize the Google Maps client
    gmaps = googlemaps.Client(key=GOOGLEMAPS_API_KEY)
    # Address to convert
    address = data['city']
    # Geocoding the address
    geocode_result = gmaps.geocode(address)
    # Extracting latitude and longitude
    if geocode_result:
        latitude = geocode_result[0]['geometry']['location']['lat']
        longitude = geocode_result[0]['geometry']['location']['lng']
    else:
        latitude = 45.5307272
        longitude = -73.6161212
    
    base_prompt = "Given a user-specified location, return RELEVANT events (hotels, flights, restaurants, or activities) that are near the specified location. Ensure diversity by including a mix of hotels, flights, restaurants, and activities. DO NOT BE BAD, GIVE ONLY EVENTS THAT ARE NEARBY. LOCATION MATTERS. You must spread out the opening hours so all these attractions can be visited through the given date range."
    if 'additional_info' in data:
        prompt = f"{data['city']} trip from {data['start_date']} to {data['end_date']} with a budget of ${data['min_budget']} to ${data['max_budget']}. Targetted with these additional information: {data['additional_info']}"
    else:
        prompt = f"{data['city']} trip from {data['start_date']} to {data['end_date']} with a budget of ${data['min_budget']} to ${data['max_budget']}."
    prompt = base_prompt + prompt

    search_results = cohere_model.retrieve_documents(prompt, curr_pos={"latitude": latitude, "longitude": longitude}, num_documents=num_docs)

    combine_prompt = f"Given the following attraction data: create an itinerary of {num_days} days starting from {data['start_date']} to {data['end_date']}. Fit all the costs within {data['min_budget']} and {data['max_budget']}. Plan according to the budget but every day should have at least one activity and at least two meals. Return the itinerary STRICTLY in the JSON format: above. Ensure the output is valid JSON and does not contain extra explanations. ONLY JSON MATCHING THE GIVEN OUTPUT FORMAT. - Ensure the output is valid JSON and does not contain extra explanations. - Do NOT prepend the data with the word json - The first character MUST be " + "{ DO NOT CHANGE THE DOCUMENT CONTENT. DO NOT CHANGE THE DOCUMENT CONTENT AND MISS METADATA. YOU MUST include eventName, minCost, maxCost, sector, openingHours, location, latitude, longitude, and description. DO NOT CHANGE THE DOCUMENT CONTENT."

    documents = ["actual attraction data: " + json.dumps(search_results), "fake format data DO NOT USE: " + json.dumps(output_format)]

    response = cohere_model.send_prompt(combine_prompt, documents)
    print(response)
    try:

        response = response[response.index("{"):]
        response = response[:response.index("`", 4)]
        response = response.replace("\n", "")
    except:
        # return jsonify({'error': 'No response from Cohere'}), 500
        pass
        
    print(response)

    new_intinerary = Itinerary(
        short_URL=generate_short_URL(),
        data=response
    )
    db.session.add(new_intinerary)

    db.session.commit()

    # return itinerary, short_URL, and trip request ID

    result = {
        'itinerary': new_intinerary.data,
        'itinerary_short_URL': new_intinerary.short_URL,
        'trip_short_ID': new_trip_request.short_ID}

    return jsonify(result), 201

# get trip request by id
@api_bp.route('/trip/<short_ID>', methods=['GET'])
def get_trip_request(short_ID):
    if not short_ID:
        return jsonify({'error': 'No short ID provided'}), 400
    
    trip = TripRequest.query.filter_by(short_ID=short_ID).first()

    if not trip:
        return jsonify({'error': 'Trip request not found'}), 404

    return jsonify(trip.data), 200

@api_bp.route('/itinerary/<short_URL>', methods=['GET'])
def get_itinerary(short_URL):
    if not short_URL:
        return jsonify({'error': 'No short URL provided'}), 400
    
    itinerary = Itinerary.query.filter_by(short_URL=short_URL).first()
    
    if not itinerary:
        return jsonify({'error': 'Itinerary not found'}), 404
    
    return jsonify(itinerary.data), 200