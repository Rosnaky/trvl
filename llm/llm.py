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
            metadata={
                "name": name
            }
        )
        # embedded_doc = self.vector_store.embedding_function.embed_query(document.page_content)
    
        self.vector_store.add_documents([document])

    def retrieveDocuments(self, prompt: str, num_documents: int = 5):
        # structured_model = self.langchainModel.with_structured_output(Project)

        docs = self.retriever.invoke(prompt, k=num_documents)

        docs_text = (d.page_content for d in docs)

        # system_prompt_fmt = system_prompt.format(context=docs_text)

        response = self.cohereModel.chat(
            model=self.model_name,
            documents=docs_text,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1024,
            temperature=0.1
        )

        return response

load_dotenv()

