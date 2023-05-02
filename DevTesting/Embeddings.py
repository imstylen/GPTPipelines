import pandas as pd
import fitz
import openai 
import tiktoken
import openai
from tenacity import retry, wait_random_exponential, stop_after_attempt, retry_if_not_exception_type
from keychain import API_KEY
from tqdm import tqdm
# Chroma's client library for Python
import chromadb
from chromadb.config import Settings
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet",
                                    persist_directory="DevTesting/Chroma"
                                ))

EMBEDDING_MODEL = 'text-embedding-ada-002'
EMBEDDING_CTX_LENGTH = 8191
EMBEDDING_ENCODING = 'cl100k_base'

# let's make sure to not retry on an invalid request, because that is what we want to demonstrate
@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(6), retry=retry_if_not_exception_type(openai.InvalidRequestError))
def get_embedding(text_or_tokens, model=EMBEDDING_MODEL):
    return openai.Embedding.create(input=text_or_tokens, model=model)["data"][0]["embedding"]

def split_string(text, token_count):
  # base case
  text = text.replace("\n"," ")
  encoding = tiktoken.get_encoding(EMBEDDING_ENCODING)
  tokens = encoding.encode(text)
  if len(tokens) <= token_count:
    return [text]
  
  # recursive case
  else:
    arr = text.split()
    mid = len(arr) // 2
    
    left = ' '.join(arr[:mid])
    right = ' '.join(arr[mid:])
    
    return split_string(left, token_count) + split_string(right, token_count)

def chunked_tokens(text, encoding_name, chunk_length):
    encoding = tiktoken.get_encoding(encoding_name)
    tokens = encoding.encode(text)

# Pull all the text from the pdfs
def get_pdf_pages(file_path):
    doc = fitz.open(file_path)  # open document
    pages = []
    
    for page in doc:  # iterate the document pages
        pages.append(page.get_text())  # get plain text (is in UTF-8)
        
    return pages

def create_chunk_dict(pdf_path, page, chunk, text):
    chunk_dict = {'pdf_path': pdf_path, 'page': page, 'chunk': chunk, 'text': text}
    return chunk_dict

def main():           
    pdf_path = "C:/Dev/GPT/DevTesting/fy2023.pdf"

    pages = get_pdf_pages(pdf_path)
    
    data = []

    for i,page in enumerate(pages):
        chunks = split_string(page,500)
        for j,chunk in enumerate(chunks):
            data.append(create_chunk_dict(pdf_path,i,j,chunk))

    df = pd.DataFrame(data)
    
    df.to_csv("DevTesting/Data.csv")
    
    print(df.head(10))
    embedding_function = OpenAIEmbeddingFunction(api_key = API_KEY, model_name=EMBEDDING_MODEL)

    content_collection = client.create_collection(name='content', embedding_function=embedding_function)

    batch_size = 100

    for i in tqdm(range(0, len(df), batch_size)):
        batch_df = df[i:i+batch_size]

        ids = [str(id) for id in batch_df.index]
        
        content_collection.add(
            ids=ids, # Chroma takes string IDs. 
            documents=(batch_df['text'] ).to_list(), # We concatenate the title and abstract.
        )

    print("Done")
    

if __name__ == "__main__":
    main()


