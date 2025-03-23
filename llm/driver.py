from llm import CohereAPI
from dotenv import load_dotenv
import os

load_dotenv()

COHERE_API_KEY = os.environ.get("COHERE_API_KEY")
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")

if __name__ == "__main__":
    model = CohereAPI(cohere_api_key=COHERE_API_KEY, pinecone_api_key=PINECONE_API_KEY)


    text1 = """Event 1: Annual Tech Conference

Event Name: Annual Tech Conference

Location: Tech Convention Center, Silicon Valley

Opening Hours: 09:00-18:00

Min Cost: $100

Max Cost: $500

Sector: Activity

The Annual Tech Conference will be held at the Tech Convention Center in Silicon Valley. Attendees can join from 09:00 AM to 6:00 PM, with ticket prices ranging from $100 to $500 depending on the package chosen. This event focuses on the latest technological advancements and innovations in the field, providing attendees with numerous networking opportunities and hands-on workshops.

"""
    text2 = """Event 2: Gourmet Dinner Night

Event Name: Gourmet Dinner Night

Location: Grand Oak Restaurant, Downtown

Opening Hours: 18:00-23:00

Min Cost: $50

Max Cost: $200

Sector: Restaurant

Join us for an exclusive Gourmet Dinner Night at Grand Oak Restaurant located in Downtown. The event will run from 6:00 PM to 11:00 PM, offering a luxurious dining experience with a cost ranging from $50 for a standard meal to $200 for a complete course. This event is perfect for food enthusiasts who wish to indulge in a fine dining experience while enjoying live music and great company."""
    
    text3 = """Event 3: Family Fun Day at the Park

Event Name: Family Fun Day at the Park

Location: Central Park, New York City

Opening Hours: 10:00-16:00

Min Cost: $20

Max Cost: $50

Sector: Activity

Bring the whole family to Family Fun Day at the Park at Central Park, New York City. This event will take place from 10:00 AM to 4:00 PM, with an affordable entry fee ranging from $20 to $50. Activities include face painting, games, and outdoor entertainment, making it a perfect outing for families looking to enjoy a day of fun and relaxation in nature.

"""

    text4 = """1. Hotel: Grand Ocean Resort
Escape to Grand Ocean Resort, a luxury beachfront hotel in Miami, Florida. Open 24/7, this five-star resort offers stunning ocean views, infinity pools, and world-class dining. Room rates start at $250 per night, with premium suites reaching $1,200. Ideal for relaxation, honeymoons, and business retreats."""
    text5 = """New York to London – British Airways
Take a premium international journey with British Airways, offering daily non-stop flights from JFK Airport, New York to Heathrow Airport, London. Flights depart from 08:00-22:00 daily, with economy fares starting at $550 and first-class seats at $3,000. Experience top-tier comfort and in-flight entertainment."""
    text6 = """The Golden Fork – Paris
Dine at The Golden Fork, a Michelin-star restaurant in Paris, France, renowned for its authentic French cuisine. Open from 18:00-23:30, enjoy exquisite dishes like foie gras, escargot, and aged wine. A meal costs between $70 and $250, offering a refined dining experience in the heart of Paris."""
    text7 = """Skydiving in Dubai
Experience an adrenaline rush with a tandem skydiving adventure over Palm Jumeirah, Dubai. Open from 07:00-17:00, this bucket-list activity costs between $400 and $650 per person. Certified instructors ensure a thrilling yet safe freefall with breathtaking city and ocean views."""
    text8 = """Alpine Ski Lodge – Switzerland
Nestled in the Swiss Alps, the Alpine Ski Lodge is a cozy winter retreat with panoramic mountain views. Open all year round, with peak ski season from November to March, room rates range from $180 to $700 per night. Perfect for skiing, snowboarding, and relaxation by the fireplace.
"""
    text9 = """Los Angeles to Tokyo – Japan Airlines
Fly from LAX, Los Angeles to Narita, Tokyo with Japan Airlines, featuring high-end service and gourmet Japanese meals. Departures run from 06:00-23:00, with ticket prices from $650 in economy to $5,000 in first class. A seamless way to explore Japan.
"""
    text10 = """Sushi Heaven – Tokyo
Visit Sushi Heaven, an award-winning omakase restaurant in Shibuya, Tokyo. Open from 12:00-22:00, this intimate dining spot serves handcrafted sushi, priced between $50 and $300 per person. Enjoy fresh seafood flown in daily from Tsukiji Market."""

    text11 = """CN Tower EdgeWalk – A thrilling activity where you walk along the edge of the CN Tower, 356m above ground. Open 09:00-20:00, costs $195 per person. (Sector: activity)"""
    text12 = """Helicopter Tour Over Toronto – A 15-minute private helicopter ride showcasing the Toronto skyline, CN Tower, and waterfront. Open 10:00-18:00, costs $130-$300 per person. (Sector: activity)"""

    # model.add_document(data=text1)
    # model.add_document(data=text2)
    # model.add_document(data=text3)

    # model.add_document(data=text4)
    # model.add_document(data=text5)
    # model.add_document(data=text6)
    # model.add_document(data=text7)
    # model.add_document(data=text8)
    # model.add_document(data=text9)
    # model.add_document(data=text10)
    # model.add_document(data=text11)
    # model.add_document(data=text12)

    base_prompt = """Given a user-specified location, return RELEVANT events (hotels, flights, restaurants, or activities) that are near the specified location. Prioritize options that are within a reasonable distance (e.g., same city, nearby town, or accessible within a short travel time). Ensure diversity by including a mix of hotels, flights, restaurants, and activities.
                    DO NOT BE BAD, GIVE ONLY EVENTS THAT ARE NEARBY. LOCATION MATTERS.
                    TORONTO TORONTO TORONTO TORONTO TORONTO TORONTO TORONTO TORONTO
                    TORONTO TORONTO TORONTO TORONTO TORONTO TORONTO TORONTO TORONTO
                    TORONTO TORONTO TORONTO TORONTO TORONTO TORONTO TORONTO TORONTO
                    TORONTO TORONTO TORONTO TORONTO TORONTO TORONTO TORONTO TORONTO
                    TORONTO TORONTO TORONTO TORONTO TORONTO TORONTO TORONTO TORONTO
                    TORONTO TORONTO TORONTO TORONTO TORONTO TORONTO TORONTO TORONTO
                    TORONTO TORONTO TORONTO TORONTO TORONTO TORONTO TORONTO TORONTO
                    TORONTO TORONTO TORONTO TORONTO TORONTO TORONTO TORONTO TORONTO
                    TORONTO TORONTO TORONTO TORONTO TORONTO TORONTO TORONTO TORONTO
                    TORONTO TORONTO TORONTO TORONTO TORONTO TORONTO TORONTO TORONTO
                    TORONTO TORONTO TORONTO TORONTO TORONTO TORONTO TORONTO TORONTO
                    TORONTO TORONTO TORONTO TORONTO TORONTO TORONTO TORONTO TORONTO
                    TORONTO TORONTO TORONTO TORONTO TORONTO TORONTO TORONTO TORONTO
                    TORONTO TORONTO TORONTO TORONTO TORONTO TORONTO TORONTO TORONTO
                    TORONTO TORONTO TORONTO TORONTO TORONTO TORONTO TORONTO TORONTO
    """

    actual_prompt = "I am a software engineering student who makes a lot of money. I am going from Waterloo to Toronto. I am single and have no budget concerns."

    res = model.retrieve_documents(
        # context=sys_prompt,
        prompt=base_prompt + actual_prompt,
        curr_pos={"latitude": 43, "longitude": -75},
        num_documents=5
    )

    with open("b.txt", "w") as f:
        f.write(str(res))
            