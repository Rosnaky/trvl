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

from schema import Data, Project

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
    
    def addDocument(self, name: str, data: str):
        document = Document(
            page_content=data,
            metadata=self.extract_structured_data(data).dict()
        )
        # embedded_doc = self.vector_store.embedding_function.embed_query(document.page_content)
    
        self.vector_store.add_documents([document])

    def retrieveDocuments(self, prompt: str, num_documents: int = 1):
        # structured_model = self.langchainModel.with_structured_output(Project)

        docs = self.retriever.invoke(prompt, k=num_documents)

        # print(docs)

        # docs_text = (d.page_content for d in docs)

        # with open("b.txt", "w", encoding="utf-8") as f:
        #     json.dump(docs[0].metadata, f, indent=4, ensure_ascii=False)

        return docs

    def parse_response_to_project(self, response: str) -> List[Project]:
        # Implement your parsing logic here to extract the required fields from the response
        projects = []

        # Example: Suppose response is a list of structured text or JSON-like structure:
        for project_data in response.split("\n"):
            # Parse project data (this can be changed to a better parsing method)
            try:
                project_info = project_data.split(",")  # Example of a comma-separated response
                project = Project(
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
                continue  # Handle any data misformatting gracefully

        return projects
    
    def extract_structured_data(self, text: str):
        system_prompt = """You are an AI that extracts structured data from text. 
            Given the following unstructured text, extract the relevant information and format it as JSON, 
            ensuring it follows this schema:

            {
                "projectName": "The name of the project",
                "entityName": "The name of the organization that is requesting a proposal",
                "url": "The url to the request of the proposal",
                "description": "A short description of the proposal or project",
                "publicationDate": "The publication date of the proposal",
                "deadlineDate": "The deadline date of the proposal",
                "sector": "The sector of the project or proposal"
            }

            - If a field is missing in the text, set it to an empty string (`""`) instead of `null`.
            - If a date is missing, infer a reasonable estimate from the context.
            - Ensure the output is valid JSON and does not contain extra explanations.
            """


        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Extract structured data from the following text:\n\n{text}")
        ]

        response = self.langchainModel.invoke(messages)

        return self.parse_json(response.content)


    def parse_json(self, json_str: str):
        json_str = json_str.replace("\n", "")
        try:
            data = json.loads(json_str)  # Convert string to dictionary

            # Fill missing fields with defaults
            data.setdefault("url", "")
            data.setdefault("deadlineData", "")

            # with open("a.txt", "w") as f:
            #     f.write(str(data))
            
            project = Project(**data)  # Validate against Pydantic model
            print(project)
            return project
        except (json.JSONDecodeError, ValidationError) as e:
            print(f"Error parsing JSON: {e}")
            return None  # Return None if there's an issue