from flask import Blueprint, request, jsonify
from app import db
from app.models import Itinerary, TripRequest
import random
import string

# blueprint for streams
api_bp = Blueprint('api', __name__, url_prefix='/api')

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

    new_intinerary = Itinerary(
        short_URL=generate_short_URL(),
        data={}
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