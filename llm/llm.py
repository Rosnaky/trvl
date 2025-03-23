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

from schema import Items, Item

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

    def retrieve_documents(self, prompt: str, num_documents: int = 5):

        docs = self.retriever.invoke(prompt, k=num_documents)

        # print(docs)

        return docs

    def parse_response_to_project(self, response: str) -> List[Item]:
        projects = []

        for project_data in response.split("\n"):
            try:
                project_info = project_data.split(",")
                project = Item(
                    projectName=project_info[0],
                    entityName=project_info[1],
                    url=project_info[2],
                    description=project_info[3],
                    publicationDate=project_info[4],
                    deadlineData=project_info[5],
                    sector=project_info[6]
                )
                projects.append(project)
            except IndexError:
                continue

        return projects
    
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
            }

            - If a field is missing in the text, set it to an empty string (`""`) instead of `null`.
            - If a date is missing, infer a reasonable estimate from the context, or leave it empty.
            - Ensure the output is valid JSON and does not contain extra explanations.
            - Do NOT prepend the data with the word json
            - The first character MUST be { STOP BEING BAD
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

            # with open("a.txt", "w") as f:
            #     f.write(str(data))
            
            project = Item(**data)
            # print(project)
            return project
        except (json.JSONDecodeError, ValidationError) as e:
            print(f"Error parsing JSON: {e}")
            return None