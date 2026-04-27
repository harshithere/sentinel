from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
import os

# Import the compiled LangGraph agent from our agents module
from agents import agent

# Initialize FastAPI app
app = FastAPI(
    title="Sentinel API",
    description="API for the Sentinel AI agent powered by Gemini 2.5 Flash",
    version="1.0.0"
)

# Define request and response models
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Sentinel API.",
        "status": "online",
        "docs": "Visit /docs to test the API."
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # Ensure API key is set before proceeding
    if "GOOGLE_API_KEY" not in os.environ:
        raise HTTPException(
            status_code=500, 
            detail="GOOGLE_API_KEY environment variable is not set."
        )

    try:
        # Create the initial state with the user's message
        initial_state = {"messages": [HumanMessage(content=request.message)]}
        
        # Invoke the agent graph
        result = agent.invoke(initial_state)
        
        # The result state contains the updated messages list.
        # The last message is the AI's response.
        ai_message = result["messages"][-1]
        
        return ChatResponse(response=ai_message.content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
