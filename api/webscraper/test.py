import json

data = [
    '{"events": [{"raw_info": "\'NUEVOS CAMINOS\' - March Tablao 2025, Mar 23", "url": "https://www.destinationtoronto.com/events/?asset=478-ig-17942762207316706", "address": "Rivoli"}, {"raw_info": "10PM Sunday Nights @ Pro hilarious comedy & variety talents show Toronto | BACKROOM COMEDY CLUB, Mar 23", "url": "https://www.destinationtoronto.com/events/?asset=478-ig-17942762207316706", "address": "Backroom Comedy Club"}], "hotels": [], "restaurants": [], "flights": []}',
    '{"events": [], "hotels": [{"raw_info": "Built in 1914, this downtown Toronto hotel blends historic charm and elegance with modern conveniences. St. Lawrence Market and the Hockey Hall of Fame are less than 10 minutes\' walk away.", "url": "https://www.booking.com/city/ca/toronto.en-gb.html", "address": "Hotel in Financial District, Toronto"}, {"raw_info": "Boasting a skylit indoor pool and 3 on-site dining options, this hotel is located across the street from Union Station.", "url": "https://www.booking.com/city/ca/toronto.en-gb.html", "address": "Hotel in Financial District, Toronto"}], "restaurants": [], "flights": []}',
    '{"events": [], "hotels": [], "restaurants": [{"raw_info": "Delicious food, lots of options. Venue isn\\u2019t large so probably best to call ahead on game or concert nights if you need a table larger than 5", "url": "https://www.opentable.ca/lolz-view-all/H4sIAAAAAAAA_1WNTQvCMBBE_8t6bco2mw-bW8EIQqka9aAiEiFCobRQRQ_if3fFkzAw8N7AvECCA4lSCyQhaYvWfYOQAf0ZBooBkiP8eQ1OZmAYKsqNMWgKnQlb5kqRVaR5MmW58mGzbKp6cfDhvN75sGdRsphUj9h28dKl-TDW8Z5mbd-nsRmePCj4_Xji5tNr7G7p_QGT057tqwAAAA==?originid=facad37f-78d8-4ad3-96bd-2d43bca90ab1", "address": "Entertainment District"}, {"raw_info": "The provided page is a search result page from OpenTable for restaurants in Toronto / Ontario that are available for late dinner on March 23, 2025. The page lists one restaurant, Pizza Rustica Restaurant & Bar, with its rating, price range, cuisine type, and available reservation times.", "url": "https://www.opentable.ca/lolz-view-all/H4sIAAAAAAAA_1WNTQvCMBBE_8t6bco2mw-bW8EIQqka9aAiEiFCobRQRQ_if3fFkzAw8N7AvECCA4lSCyQhaYvWfYOQAf0ZBooBkiP8eQ1OZmAYKsqNMWgKnQlb5kqRVaR5MmW58mGzbKp6cfDhvN75sGdRsphUj9h28dKl-TDW8Z5mbd-nsRmePCj4_Xji5tNr7G7p_QGT057tqwAAAA==?originid=facad37f-78d8-4ad3-96bd-2d43bca90ab1", "address": "Toronto / Ontario"}], "flights": []}',
    '{"events": [], "hotels": [], "restaurants": [], "flights": [{"raw_info": "Air Canada, Operated by Air Canada Express - Jazz, 8:25 AM - 9:47 AM, 1 hr 22 min, CA$322", "url": "https://www.google.com/travel/flights?sca_esv=ca5690578bab1f18&output=search&q=flight+from+Montreal+to+Toronto&source=lnms&fbs=ABzOT_CWdhQLP1FcmU5B0fn3xuWpmDtIGL1r84kuKz6yAcD_ii7OogsQ231XYxQSgD6WE5UwIF6FOM9o2C1Eb2tkmFdtQK9jiBy6RFzXKRrMDQM4OXWW1NdRUu61gwQwtasWqFzPvuzGZVVF3h0NXLc_R535DYY7ooV9ubPKz_9j0n_uUBdKgNCptfNpzDPXVSroBm_3n_hrvI3KeONSeMBVdw3kYTK8IQ&ved=1t:200715&ictx=111", "departure_location": "YUL"}]}'
]

# Convert JSON strings into Python dictionaries
parsed_data = [json.loads(item) for item in data]

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

# Print results
for event in events:
    try: 
        text = event["raw_info"] + f"latitude:  longitude:  eventUrl: {event["url"]}"
        print(text)
        # cohere_model.add_document(data=text)
        print(f"  - {event['raw_info']} (Location: {event['address']}) | {event['url']}")
    except:
        pass

for hotel in hotels:
    try:
        text = hotel["raw_info"] + f"latitude:  longitude:  hotelUrl: {hotel["url"]}"
        print(text)
        # cohere_model.add_document(data=text)

        print(f"  - {hotel['raw_info']} (Location: {hotel['address']}) | {hotel['url']}")
    except:
        pass

for restaurant in restaurants:
    try:
        text = restaurant["raw_info"] + f"latitude:  longitude:  restaurantUrl: {restaurant["url"]}"
        # cohere_model.add_document(data=text)
        print(text)

        print(f"  - {restaurant['raw_info']} (Location: {restaurant['address']}) | {restaurant['url']}")
    except:
        pass

for flight in flights:
    try:
        print(text)
        text = restaurant["raw_info"] + f"departure_location:  longitude:  restaurantUrl: {restaurant["url"]}"
        # cohere_mo
    except:
        pass