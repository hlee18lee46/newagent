from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI

def create_qa_chain(retriever):
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    return RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

def answer_query(qa_chain, query):
    return qa_chain.run(query)
