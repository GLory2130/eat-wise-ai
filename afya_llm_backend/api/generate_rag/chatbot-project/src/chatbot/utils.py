from typing import List
import os

def load_documents(directory: str) -> List[str]:
    documents = []
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):  # Assuming documents are in .txt format
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                documents.append(file.read())
    return documents

def format_response(response: str) -> str:
    return response.strip().capitalize() + '.' if response else 'I am sorry, I do not have an answer for that.' 

def preprocess_query(query: str) -> str:
    return query.lower().strip()