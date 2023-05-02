from keychain import API_KEY
import pandas as pd
import openai 
from tenacity import retry, wait_random_exponential, stop_after_attempt, retry_if_not_exception_type
# Chroma's client library for Python
import chromadb
from chromadb.config import Settings
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction


def main():
    
    EMBEDDING_MODEL = 'text-embedding-ada-002'

    embedding_function = OpenAIEmbeddingFunction(api_key = API_KEY, model_name=EMBEDDING_MODEL)

    df = pd.read_csv("DevTesting/Data.csv")

    client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet",
                                        persist_directory="DevTesting/Chroma"
                                    ))

    content_collection = client.get_collection("content",embedding_function=embedding_function)
    
    while True:
        query = input("Type a query:")
        
        query_result = content_collection.query(query_texts=[query], include=['documents', 'distances'], n_results=3)
        
        for match,id in enumerate(query_result['ids'][0]):
            print(f"Match: {match}")
            print("========================\n")
            print(a:=df.loc[int(id)])
            print("------------------------\n")
            print(a.text)
            print("========================\n")
        
        