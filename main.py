from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from utils.chatbot import initialize_qa_chain
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from utils.github_data import fetch_github_repos
from utils.vector_store import vectorize_github_repos, store_vectors_faiss
from utils.qa_chain import create_qa_chain, answer_query
import asyncio
# Load environment variables
load_dotenv()

app = FastAPI()

# Input data model
class QueryRequest(BaseModel):
    query: str

# Global variables
qa_chain = None

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI application!"}


@app.on_event("startup")
async def startup_event():
    global qa_chain
    repos = await fetch_github_repos()
    docs, embeddings = vectorize_github_repos(repos)
    vectorstore = store_vectors_faiss(docs, embeddings)

    # Create a retriever using LangChain's FAISS wrapper
    retriever = vectorstore.as_retriever()

    # Create the QA chain
    qa_chain = create_qa_chain(retriever)


@app.post("/query")
async def query_agent(request: QueryRequest):
    if "how many repos" in request.query.lower():
        repos = await fetch_github_repos()
        print(f"Number of repositories fetched: {len(repos)}")
        num_repos = len(repos)
        return {"query": request.query, "answer": f"You have {num_repos} repositories on your GitHub account."}
    
    # Default QA chain processing
    if not qa_chain:
        raise HTTPException(status_code=500, detail="QA chain not initialized.")
    try:
        answer = qa_chain.run(request.query)
        return {"query": request.query, "answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
