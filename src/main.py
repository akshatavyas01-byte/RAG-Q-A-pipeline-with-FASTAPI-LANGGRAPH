from fastapi import FastAPI,UploadFile, Path, Query
from .graphs import vector_graph, question_graph, State
from langchain_community.vectorstores import Chroma
from langchain_classic.schema import Document
from typing import Annotated
import tempfile

import uuid
app=FastAPI()
Vectorstore:dict[str,Chroma]={}


retriever=None

@app.post("/upload/")
async def upload_for_QA( file:UploadFile):
    try:
        value=False
        session_id=uuid.uuid4()
        if file.content_type=="application/pdf": 
            with tempfile.NamedTemporaryFile(delete=False,suffix=".pdf") as temp:
                content=await file.read()
                temp.write(content)
                temp_path=temp.name
            if temp_path:
              state: State = {
                "path": temp_path,
                "chunks": [],
                }
              result=vector_graph.invoke(state)
              Vectorstore[str(session_id)]=result["vectorstore"]  
              vector=Vectorstore.get(str(session_id))
              if vector:
                  value=True
            return {"session_id":session_id,
                        "text":"file uploaded Successfully for Q&A!!",
                        "vectorstore":value} 
    except Exception as e:
        return  {"answer":str(e)}
 
 
@app.get("/ask/{session_id}")
async def ask_question(
    session_id:Annotated[str, Path(title="Session_id",description="Session_id of user for vector store")],
    question:Annotated[str,Query(title="Question",description="Question for the pdf")]
):
    try:
        if session_id in Vectorstore:
            vectorstore=Vectorstore[session_id]
            if question and vectorstore:
                state:State={
                    "question":question,
                    "vectorstore":vectorstore
                    }
                response=question_graph.invoke(state)
                answer=response["answer"]
                return {"answer":answer}
    except Exception as e:
        return  {"answer":str(e)}
            
         