from langchain.chains import RetrievalQA
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document  # Import the Document class
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import JSONLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI


async def initialize_qa_chain(github_data):
    documents = []
    for repo in github_data:
        # Ensure valid content for page_content
        description = repo.get("description")
        if not isinstance(description, str) or not description.strip():
            description = "No description provided."
        
        # Append a valid Document
        documents.append(
            Document(
                page_content=description,
                metadata={
                    "name": repo.get("name", "Unknown"),
                    "url": repo.get("html_url", "No URL provided")
                }
            )
        )
    print("Documents for QA Chain:", documents)

    # Create embeddings and retriever
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(documents, embeddings)
    retriever = vectorstore.as_retriever()

    # Initialize the LLM
    llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")  # Adjust model as needed

    # Build the QA chain
    return RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

