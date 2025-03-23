from llm import CohereAPI
from dotenv import load_dotenv
import os

load_dotenv()

COHERE_API_KEY = os.environ.get("COHERE_API_KEY")
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")

# if __name__ == "__main__":
#     model = CohereAPI(cohere_api_key=COHERE_API_KEY, pinecone_api_key=PINECONE_API_KEY)


# #     text1 = """Event 1: Annual Tech Conference

# # Event Name: Annual Tech Conference

# # Location: Tech Convention Center, Silicon Valley

# # Opening Hours: 09:00-18:00

# # Min Cost: $100

# # Max Cost: $500

# # Sector: Activity

# # The Annual Tech Conference will be held at the Tech Convention Center in Silicon Valley. Attendees can join from 09:00 AM to 6:00 PM, with ticket prices ranging from $100 to $500 depending on the package chosen. This event focuses on the latest technological advancements and innovations in the field, providing attendees with numerous networking opportunities and hands-on workshops.

# # """
# #     text2 = """Event 2: Gourmet Dinner Night

# # Event Name: Gourmet Dinner Night

# # Location: Grand Oak Restaurant, Downtown

# # Opening Hours: 18:00-23:00

# # Min Cost: $50

# # Max Cost: $200

# # Sector: Restaurant

# # Join us for an exclusive Gourmet Dinner Night at Grand Oak Restaurant located in Downtown. The event will run from 6:00 PM to 11:00 PM, offering a luxurious dining experience with a cost ranging from $50 for a standard meal to $200 for a complete course. This event is perfect for food enthusiasts who wish to indulge in a fine dining experience while enjoying live music and great company."""
    
# #     text3 = """Event 3: Family Fun Day at the Park

# # Event Name: Family Fun Day at the Park

# # Location: Central Park, New York City

# # Opening Hours: 10:00-16:00

# # Min Cost: $20

# # Max Cost: $50

# # Sector: Activity

# # Bring the whole family to Family Fun Day at the Park at Central Park, New York City. This event will take place from 10:00 AM to 4:00 PM, with an affordable entry fee ranging from $20 to $50. Activities include face painting, games, and outdoor entertainment, making it a perfect outing for families looking to enjoy a day of fun and relaxation in nature.

# # """

# #     # model.add_document(data=text1)
# #     # model.add_document(data=text2)
# #     # model.add_document(data=text3)

#     human_prompt = "Return a list of events that are most relevant to the following prompt. Consider all factors."

#     actual_prompt = "I am a software engineering student who makes a lot of money. I am single and have no budget concerns."

#     res = model.retrieve_documents(
#         # context=sys_prompt,
#         prompt=human_prompt + actual_prompt,
#         curr_pos={"latitude": 37.7749, "longitude": -122.4194},
#         num_documents=2
#     )

#     with open("b.txt", "w") as f:
#         f.write(str(res))
            