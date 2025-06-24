import os
import json
import requests

from openai import OpenAI
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_community.document_loaders import FireCrawlLoader
from langchain_community.document_loaders import SpiderLoader
from langchain_core.documents import Document

from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

loader = FireCrawlLoader(
    url="https://fbref.com/en/comps/9/Premier-League-Stats",
    api_key=os.getenv("FIRECRAWL_API_KEY")
)

docs = loader.load()


system_prompt = """
You are a helpful assistant that answers questions about the Premier League.
Given a user query, your task is to generate 3 semantically diverse sub-queries that can be used to retrieve relevant documents.
Return the output as a JSON object with the format:
{
    "queries": [
        "First sub-query",
        "Second sub-query",
        "Third sub-query"
    ]
}
"""
messages = [
    {"role" : "system" , "content": system_prompt}
]
# SPLITTER
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)
split_docs = text_splitter.split_documents(docs)

#Embeddding
embedder = OpenAIEmbeddings(
    model= "text-embedding-3-large",
    api_key=os.getenv("OPENAI_API_KEY")
)

# Storing the embeddings in Qdrant
vector_store = QdrantVectorStore.from_documents(
    documents=[],
    url="http://localhost:6333",
    collection_name="PL-RAG",
    embedding=embedder
)
vector_store.add_documents(documents = split_docs)

retriever = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="PL-RAG",
    embedding=embedder
    )


from langchain_core.documents import Document
while True:
    user_query = input(">>")
    messages.append(
        {"role": "user", "content": user_query}
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=messages
    )
    
    parsed_response = json.loads(response.choices[0].message.content)  # gives a dict with 3 queries splitted
    messages.append(
        {"role": "assistant", "content": response.choices[0].message.content}
    )
    
    sub_queries = parsed_response["queries"]
    docs = [Document(page_content=q) for q in sub_queries]

    #Using retriever to get relevant documents for each sub-query
    all_chunks = []
    for q in sub_queries:
        results = retriever.similarity_search(query=q, k=3)
        all_chunks.extend(results)  # collect all chunks here
        print(f"Sub-query: {q}")
        for res in results:
            print(res.page_content)
        print("\n---\n")
    
    # Embed and store the sub-queries
    vector_store.add_documents(documents=docs)
    
    # Retrieve relevant documents based on the sub-queries
    # retrieved_docs = retriever.get_relevant_documents(user_query)

    # Process and display the retrieved documents as needed
    # for doc in retrieved_docs:
    #     print(doc.page_content)
    
    system_prompt2 = """
    You are a helpful assistant. You have been provided with relevant context chunks retrieved from a knowledge base in response to a user's question. 
    Using only this information, answer the user's query as accurately and concisely as possible. If the answer is not found in the context, respond accordingly.
    """
    # Step 1: Combine all chunks
    context_chunks = "\n\n".join([chunk.page_content for chunk in all_chunks])

    # Step 2: Create a new message list
    final_messages = [
        {"role": "system", "content": system_prompt2},
        {"role": "user", "content": f"User Query: {user_query}\n\nRelevant Chunks:\n{context_chunks}"}
    ]

    final_reponse = client.chat.completions.create(
        model="gpt-4o",
        messages=final_messages)

    print(f"Final Response: {final_reponse.choices[0].message.content}")