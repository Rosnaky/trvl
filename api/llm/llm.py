import json
import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_cohere import CohereEmbeddings
from langchain_pinecone import PineconeVectorStore
import cohere
from langchain_core.documents import Document
from typing import List
from langchain_core.messages import SystemMessage, HumanMessage
from langchain.chat_models import init_chat_model
from pydantic import ValidationError
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from geopy.distance import geodesic

from llm.schema import Items, Item

THRESHOLD_SIMILARITY = 0.4

class CohereAPI:
    def __init__(self, cohere_api_key: str, pinecone_api_key: str, model_name: str = "command-r-plus"):
        self.pc = Pinecone(api_key=pinecone_api_key)
        index = self.pc.Index("travel")
        self.langchainModel = init_chat_model(model_name, model_provider="cohere")
        self.cohereModel = cohere.ClientV2(api_key=cohere_api_key)
        self.model_name = model_name

        embeddings = CohereEmbeddings(model="embed-english-v3.0")
        self.vector_store = PineconeVectorStore(embedding=embeddings, index=index)
        self.retriever = self.vector_store.as_retriever(
            search_type="similarity"
        )
    
    def add_document(self, data: str):
        document = Document(
            page_content=data,
            metadata=self.extract_structured_data(data).model_dump()
        )
    
        self.vector_store.add_documents([document])

    def retrieve_documents(self, prompt: str, curr_pos: dict, num_documents: int = 5):

        docs = self.retriever.invoke(prompt, k=num_documents)

        # print(docs)

        # return [d.metadata for d in docs]
        embedder = CohereEmbeddings(model="embed-english-v3.0")
        query_embedding = embedder.embed_query(prompt)

    # Step 2: Retrieve documents
        docs = self.retriever.invoke(prompt, k=num_documents)

        results = []
        for d in docs:
            metadata = d.metadata

            doc_embedding = embedder.embed_query(d.page_content)  # Ensure your retriever provides this!
            similarity = cosine_similarity(
                np.array(query_embedding).reshape(1, -1),
                np.array(doc_embedding).reshape(1, -1)
            )[0][0]
            # print(metadata)

            try:
                if (metadata["latitude"] != "-1" and metadata["longitude"] != "-1"):
                    similarity = similarity*0.7 + self.custom_similarity_score(metadata["latitude"], metadata["longitude"], curr_pos)*0.3

                # print(str(similarity) + " " + str(metadata))
                if (similarity > THRESHOLD_SIMILARITY):
                    results.append(metadata)
            except:
                pass

        return results

    
    def extract_structured_data(self, text: str):
        system_prompt = """You are an AI that extracts structured data from text. 
            Given the following unstructured text, extract the relevant information and format it as JSON, 
            ensuring it follows this schema:

            {
                "eventName": "The name of the event",
                "location": "The name of the location of the event",
                "opening_hours": "The hours that the event is open in the format of HH:MM-HH:MM",
                "min_cost": "The minimum recommended cost to participate in the event",
                "max_cost": "The maximum recommended cost to participate in the event",
                "sector": "The type of activity. It must be one of the following four options: restaurant, activity, flight, hotel."
                "url": "The url for more information about the event"
                "description": "A very short description of the event, about 30 words."
                "latitude": "The latitude coordinates of the location. Must be a single floating point number."
                "longitude": "The longitude coordinates of the location. Must be a single floating point number."
            }

            - If a field is missing in the text, set it to an empty string (`""`) instead of `null`.
            - If a date is missing, infer a reasonable estimate from the context, or leave it empty.
            - Ensure the output is valid JSON and does not contain extra explanations.
            - Do NOT prepend the data with the word json
            - The first character MUST be { STOP BEING BAD
            - If latitude or longitude are missing, return -1 YOU MUST RETURN SOMETHING PLEASE
            """


        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Extract structured data from the following text: {text}")
        ]

        response = self.langchainModel.invoke(messages)

        return self.parse_json(response.content)


    def parse_json(self, json_str: str):
        json_str = json_str.replace("\n", "")
        # print(json_str)
        try:
            data = json.loads(json_str) 

            data.setdefault("location", "")
            data.setdefault("opening_hours", "")
            data.setdefault("sector", "")
            data.setdefault("min_cost", "")
            data.setdefault("max_cost", "")
            data["latitude"] = str(data.get("latitude", "-1"))
            data["longitude"] = str(data.get("longitude", "-1"))

            # with open("a.txt", "w") as f:
            #     f.write(str(data))
            
            project = Item(**data)
            # print(project)
            return project
        except (json.JSONDecodeError, ValidationError) as e:
            print(f"Error parsing JSON: {e}")
            return None
        
    def custom_similarity_score(self, lat, lon, query_location):
        try:
            # print(doc)
            doc_location = (int(lat), int(lon))  
            user_location = (query_location["latitude"], query_location["longitude"])  
            distance_km = geodesic(doc_location, user_location).km
            location_score = max(0, 1 - (distance_km / 50))  
            return location_score * 0.3 
        except:
            return 0.1
