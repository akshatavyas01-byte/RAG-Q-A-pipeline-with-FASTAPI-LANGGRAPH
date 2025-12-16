from langgraph.graph import START, END, StateGraph
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_classic.schema import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from typing_extensions import TypedDict
import os 

load_dotenv()

model_name="sentence-transformers/paraphrase-MiniLM-L3-v2"
huggingfaceembedding=HuggingFaceEmbeddings(
    model_name=model_name
)


class State(TypedDict,total=False):
    path: str
    chunks: list[Document]
    vectorstore: Chroma
    question: str
    content: list[Document]
    answer: str


def file_chunks_node(state:State):
    file_path=state.get("path")
    if  not file_path:
        raise ValueError("No file Path")
    loader=PyPDFLoader(file_path)
    docs=loader.load()

    text_splitter=RecursiveCharacterTextSplitter(chunk_size=800,chunk_overlap=100,separators=["\n","\n\n"," ",""])

    chunks=text_splitter.split_documents(docs)

    for chunk in chunks:
        chunk.metadata["filename"]=file_path
    return {
        "path":state.get("path"),
        "chunks":chunks,
        "vectorstore":None
    }



def vectorstore_node(state:State):
    chunks=state.get("chunks")
    if not chunks:
        raise ValueError("No chunks")
    vectorstore=Chroma.from_documents(chunks, huggingfaceembedding)
    return {
    "path":state.get("path"),
    "chunks":chunks,
    "vectorstore":vectorstore
    }
   

vectorgraph=StateGraph(State)

vectorgraph.add_node("file_chunks_node",file_chunks_node)
vectorgraph.add_node("vectorstore_node",vectorstore_node)
vectorgraph.add_edge(START,"file_chunks_node")
vectorgraph.add_edge("file_chunks_node","vectorstore_node")
vectorgraph.add_edge("vectorstore_node",END)



vector_graph=vectorgraph.compile()



api_key=os.getenv("GORQ_API_KEY")

llm=ChatGroq(model="llama-3.1-8b-instant",api_key=api_key)# pyright: ignore[reportArgumentType]

def retriever_node(state:State):
    try:
        VectorStore=  state.get("vectorstore")
        question=state.get("question")
        if not question or not VectorStore:
            raise ValueError("question n Vectorstore")
        else:
            content=None
            retriever=VectorStore.as_retriever(
                search="similarity",
                k=3
            )
            docs=retriever.invoke(question)
            if docs:
                for doc in docs:
                    content="\n\n".join(doc.page_content)
            return {
            "content":content
            }
    except Exception as e:
        return{"answer":str(e)}
def llm_node(state:State):
    try:
        question=state.get("question")
        content=state.get("content")
        if question and content:
            prompt=f'''
            Your a helpful assistant.
            Task answer the following question with help of the content given:
            Question:
            {question}

            Content:
            {content}
            
            '''
            result=llm.invoke(prompt)
            return {
                "answer":result.content
            }
        else:
            return {
                "answer":"No question or content"
            }
    except Exception as e:
        return {"answer":str(e)}
    
graph_question=StateGraph(State)

graph_question.add_node("retriever_node",retriever_node)
graph_question.add_node("llm_node",llm_node)

graph_question.add_edge(START,"retriever_node")
graph_question.add_edge("retriever_node","llm_node")
graph_question.add_edge("llm_node",END)


question_graph=graph_question.compile()
