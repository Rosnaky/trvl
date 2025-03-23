from flask import Blueprint, request, jsonify
from app import db
from app.models import Itinerary, TripRequest
import random
import string
import os
from dotenv import load_dotenv
from datetime import datetime

from llm.llm import CohereAPI

# blueprint for streams
api_bp = Blueprint('api', __name__, url_prefix='/api')

load_dotenv()

COHERE_API_KEY = os.environ.get("COHERE_API_KEY")
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")

cohere_model = CohereAPI(cohere_api_key=COHERE_API_KEY, pinecone_api_key=PINECONE_API_KEY)

tokyo_attractions = [
    {
        "name": "Tokyo Skytree",
        "description": "The tallest tower in Japan, offering panoramic views of Tokyo from its observation decks.",
        "price": {"min_price": 2200, "max_price": 2200},
        "location": "Sumida City"
    },
    {
        "name": "Senso-ji Temple",
        "description": "One of Tokyo's oldest and most significant Buddhist temples, known for its vibrant gates and incense smoke.",
        "price": {"min_price": 0, "max_price": 0},
        "location": "Asakusa"
    },
    {
        "name": "Shibuya Crossing",
        "description": "The world's busiest pedestrian crossing, a symbol of Tokyo's bustling urban life.",
        "price": {"min_price": 0, "max_price": 0},
        "location": "Shibuya"
    },
    {
        "name": "Tsukiji Outer Market",
        "description": "A lively seafood and food market with fresh sushi, snacks, and kitchenware.",
        "price": {"min_price": 100, "max_price": 5000},
        "location": "Tsukiji"
    },
    {
        "name": "Meiji Shrine",
        "description": "A serene Shinto shrine surrounded by a vast forest, dedicated to Emperor Meiji and Empress Shoken.",
        "price": {"min_price": 0, "max_price": 0},
        "location": "Shibuya"
    },
    {
        "name": "Odaiba",
        "description": "A modern entertainment district on a man-made island, featuring shopping malls, amusement centers, and the iconic Gundam statue.",
        "price": {"min_price": 0, "max_price": 3000},
        "location": "Tokyo Bay"
    },
    {
        "name": "Akihabara",
        "description": "The hub of Japan's otaku culture, filled with electronics stores, anime shops, and gaming centers.",
        "price": {"min_price": 0, "max_price": 10000},
        "location": "Akihabara"
    },
    {
        "name": "Ueno Park",
        "description": "A large public park home to museums, temples, and the beautiful Shinobazu Pond.",
        "price": {"min_price": 0, "max_price": 1000},
        "location": "Ueno"
    },
    {
        "name": "Roppongi Hills",
        "description": "A modern urban development with shopping, dining, art museums, and the Mori Tower observation deck.",
        "price": {"min_price": 0, "max_price": 5000},
        "location": "Roppongi"
    },
    {
        "name": "Imperial Palace",
        "description": "The primary residence of Japan's Imperial Family, surrounded by moats and large gardens.",
        "price": {"min_price": 0, "max_price": 0},
        "location": "Chiyoda"
    }
]

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
    
    required_params = ['city', 'start_date', 'end_date', 'min_budget', 'max_budget']

    for param in required_params:
        if param not in data:
            return jsonify({'error': f'Missing required parameter: {param}'}), 400

    new_trip_request = TripRequest(
        short_ID=generate_short_ID(),
        data=data
    )
    db.session.add(new_trip_request)

    # find num_docs by calculating substrings of data['start_date'] and data['end_date'], num_docs = num_days * 10
    start_date = datetime.strptime(data['start_date'], '%m%d%Y')
    end_date = datetime.strptime(data['end_date'], '%m%d%Y')

    # Calculate the difference in days
    num_days = (end_date - start_date).days

    num_docs = num_days * 10
    
    base_prompt = "Given a user-specified location, return RELEVANT events (hotels, flights, restaurants, or activities) that are near the specified location. Prioritize options that are within a reasonable distance (e.g., same city, nearby town, or accessible within a short travel time). Ensure diversity by including a mix of hotels, flights, restaurants, and activities. DO NOT BE BAD, GIVE ONLY EVENTS THAT ARE NEARBY. LOCATION MATTERS. You must spread out the opening hours so all these attractions can be visited through the given date range."
    if 'additional_info' in data:
        prompt = f"{data['city']} trip from {data['start_date']} to {data['end_date']} with a budget of ${data['min_budget']} to ${data['max_budget']}. Targetted with these additional information: {data['additional_info']}"
    else:
        prompt = f"{data['city']} trip from {data['start_date']} to {data['end_date']} with a budget of ${data['min_budget']} to ${data['max_budget']}."
    prompt = base_prompt + prompt

    search_results = cohere_model.retrieve_documents(prompt, curr_pos={"latitude": 43, "longitude": -75}, num_documents=num_docs)

    new_intinerary = Itinerary(
        short_URL=generate_short_URL(),
        data=search_results
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