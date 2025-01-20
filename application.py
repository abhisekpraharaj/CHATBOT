from fastapi import FastAPI 
from pydantic import BaseModel 
from typing import List  
from langchain_community.tools.tavily_search import TavilySearchResults  
import os  
from langgraph.prebuilt import create_react_agent 
from langchain_groq import ChatGroq 

groq_api_key = 'xxxxxxxxxxxxxxxxx'  # Groq API key
os.environ["TAVILY_API_KEY"] = 'xxxxxxxxxxxxxxxxxx'  # Set Tavily API key

MODELS = [
    "llama3-70b-8192",  # Model 1: Llama 3 with specific configuration
    "mixtral-8x7b-32768",  # Model 2: Mixtral with specific configuration
    "distil-whisper-large-v3-en", # Model 3
    "gemma2-9b-it" #Model 4
]

tool_tavily = TavilySearchResults(max_results=3)

tools = [tool_tavily,]

application = FastAPI(title = "LangGraph AI Agent for Practice")

class request_state(BaseModel):
    model: str
    prompt: str
    messages: List[str]

@application.post("/machine")
def machine_endpoint(request:request_state):
    print(request)
    if not request.model or not request.prompt:
        return {"error": "Model and prompt must be provided."}  
    if request.model not in MODELS:
        return{"error": "Please select the model out of the selection box."}

    llm = ChatGroq(groq_api_key= groq_api_key, model = request.model)
    agent = create_react_agent(llm, tools = tools, state_modifier = request.prompt)
    state = {"messages":request.messages}

    result = agent.invoke(state)
    return result

if __name__ == '__main__':
    import uvicorn 
    uvicorn.run(application, host = '127.0.0.1', port =8000)



    

