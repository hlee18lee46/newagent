from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document

def vectorize_github_repos(repos):
    embeddings = OpenAIEmbeddings()
    docs = [
        Document(
            page_content=f"Repository Name: {repo['name']}. Description: {repo['description']}. URL: {repo['url']}",
            metadata={"name": repo["name"], "url": repo["url"]}
        )
        for repo in repos
    ]
    return docs, embeddings

def store_vectors_faiss(docs, embeddings):
    # Use LangChain's FAISS wrapper to store vectors
    vectorstore = FAISS.from_documents(docs, embeddings)
    return vectorstore
