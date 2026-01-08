# RAG Q&A pipeline with FASTAPI + LANGGRAPH

A basic Retrieval-Augmented Generation (RAG) Q&A pipeline built using FastAPI, 
LangGraph, CHroma Vectorstore and the Groq LLM. This project is part of a learning series and 
demonstrates PDF-based question answering using vector embeddings and retrieval.


---

## FEATURES
1. App Features:
    - Upload PDF files via a POST API endpoint
    - Send questions through a GET API endpoint
    - Receive answers generated based on the uploaded PDF content

2. Langchain concepts:
    - Text Splitters
    - Schema
    - Document Loaders
    - Vectorstores

3. Langgraph Concepts:
    - Graph(START, END, StateGraph)
    - Nodes
    - Edges
    - TypedDict -State Based

4. Langchain HuggingFace:
    - HuggingFaceEmbeddings

5. Langchain GROQ:
    - ChatGroq

6. FAST API
    - POST and GET
    - UploadFile handling
    - Path and Query parameters
    - Auto-generated API documentation (Swagger UI)

7. Backend utilites
    - tempfile for temporary PDF storage

    - uuid for session-based vector store management

8.  Testing
    - POSTMAN
    - Swagger UI

    ---
## TECHNOLOGIES USED
    Python 3.x
    Uvicorn   
    Langgraph
    Langchain
    Langchain_classic
    Langchain-community
    Langchain-Groq
    Langchain-HuggingFace
    Typing Extensions

---
## FOLDER STRUCTURE

    project/
            |── src/
            |   |── main.py
            |   |── graphs.py
            |
            |── images/
            |
            |── TestFiles/
            |   |── neet-photosynthesis_notes.pdf
            |   |── TechNet-One-Pager-on-AI-and-Gen-AI.pdf
            |
            |── .env
            |
            |── requirements.txt
            |
            └── ReadMe.md
---
## Installation & Setup for the project

```python
git clone RAG Q&A pipeline with FASTAPI + LANGGRAPH
cd project-name

pip install -r requirements.txt

uvicorn src.main:app --reload

```

## Environment Setup
```python

python -m venv venv

venv/Scripts/Activate.ps1

```
## Install Dependencies
```python

pip install -r requirements.txt

```
---
## Environment Variables (.env Setup)
This project requires an API key to access HuggingFace LLMs.

### 1. Create a .env file in the project root
```python
GROQ_API_KEY=your_api_key_here
```

### 2. Ensure the key loads in your code

Example (in chat_llm.py):
```python
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
```
### 3. Install dotenv if not installed
```python
pip install python-dotenv

```
---

## API Endpoints

| Method | Endpoint | Parameters| Description |
|---|---|---|---|
| POST | `/upload/` | **Body (form-data):** `file` (PDF) | Uploads a PDF file to initialize the RAG pipeline and returns a session ID along with the vector store creation status. |
| GET | `/ask/{session_id}` | **Path:** `session_id`<br>**Query:** `question` | Sends a question related to the uploaded PDF and returns an answer generated using the RAG pipeline. |

---
## Request and Example
### Upload PDF
 - POST(`"/upload/"`)
    - Body (form-data):
        - `file:` PDF file

### Response
```json
{
  "session_id": "ec13f400-c625-4bfd-9eea-4b1e6a163263",
  "text": "file uploaded Successfully for Q&A!!",
  "vectorstore": true
}
```
### Ask Question
 - GET(`"/ask/{session_id}"`)
    - Query 
        - `question`= Explain%20Electron%20Transport%20System

### Response     
```json
{
    "answer": "Based on the content provided, I'll help you explain the Electron Transport System (ETS).\n\n**The Electron Transport System:**\n\nThe Electron Transport System is a series of protein complexes located in the mitochondrial inner membrane. It plays a crucial role in the process of cellular respiration, specifically in the electron transport chain.\n\n**How it works:**\n\nThe Electron Transport System is responsible for generating a proton gradient across the mitochondrial inner membrane. This gradient is used to produce ATP (adenosine triphosphate), which is the energy currency of the cell.\n\n**The components involved:**\n\nThe Electron Transport System consists of:\n\n1. **ATP Synthase (PSII)**: This enzyme uses the proton gradient to produce ATP from ADP and Pi.\n2. **Cytochrome b-c1 complex (Complex III)**: This complex is involved in the transfer of electrons from Coenzyme Q (CoQ) to Cytochrome c (Cyt c).\n3. **Cytochrome c oxidase (Complex IV)**: This complex is responsible for the transfer of electrons from Cyt c to Oxygen (O2), resulting in the formation of water.\n4. **NADH dehydrogenase (Complex I)**: This complex is involved in the transfer of electrons from NADH to CoQ.\n5. **Succinate dehydrogenase (Complex II)**: This complex is involved in the transfer of electrons from Succinate to CoQ.\n\n**The process:**\n\nThe Electron Transport System works as follows:\n\n1. **Electrons from NADH and FADH2 are passed to Complex I and Complex II**, respectively.\n2. **The electrons are then transferred to CoQ**, which is reduced to CoQH2.\n3. **The electrons are passed to Complex III**, where they are transferred to Cyt c.\n4. **The electrons are then passed to Complex IV**, where they are transferred to O2, resulting in the formation of water.\n5. **The proton gradient is used by ATP Synthase to produce ATP from ADP and Pi**.\n\n**Regulation of the Electron Transport System:**\n\nThe Electron Transport System is regulated by various mechanisms, including:\n\n1. **Regulation by the Respiratory Control Protein (RUC)**: This protein regulates the electron transport chain by adjusting the flow of electrons.\n2. **Regulation by the Mitochondrial Membrane Potential**: The membrane potential regulates the flow of electrons by controlling the movement of protons across the membrane.\n\n**Inhibitors of the Electron Transport System:**\n\nThe Electron Transport System can be inhibited by various compounds, including:\n\n1. **Rotenone**: This compound inhibits Complex I.\n2. **Antimycin A**: This compound inhibits Complex III.\n3. **Oligomycin**: This compound inhibits ATP Synthase.\n\nOverall, the Electron Transport System is a complex process that plays a crucial role in the production of ATP in cells. It is regulated by various mechanisms to ensure efficient energy production."
}
```


---

# Demo Images
### 1. Uvicorn:
![alt text](/images/image.png)

### 2. FAST API(SWAGGER DOCS):
![alt text](/images/image1.png)
![alt text](/images/image2.png)
![alt text](/images/image3.png)

### 3. Swagger UI POST Tryout:
![alt text](/images/image4.png)
![alt text](/images/image5.png)

### 4. Swagger UI GET Tryout:
![alt text](/images/image6.png)
![alt text](/images/image7.png)

### 5. Postman POST request:
![alt text](/images/image8.png)

### 6. Postman GET request:
![alt text](/images/image9.png)
       
---

## Possible Improvements
- Add persistent vector storage
- Improve error handling and validation
- Support multi-document uploads
---

## License
This project is licensed under the MIT License.

---
## Author
**Akshata Vyas**  
GitHub: [akshatavyas01-byte](https://github.com/akshatavyas01-byte)
