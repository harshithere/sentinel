import os
from typing import Annotated, TypedDict

from dotenv import load_dotenv
load_dotenv()

from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import START, END, StateGraph
from langgraph.graph.message import add_messages

# Instructions to run:
# 1. Install dependencies: pip install langgraph langchain-google-genai
# 2. Set your Google API key: export GOOGLE_API_KEY="your-api-key"
# 3. Run the script: python agent.py

# Define the state structure for our graph
class State(TypedDict):
    # The `add_messages` function appends new messages to the list,
    # rather than overwriting it.
    messages: Annotated[list, add_messages]

# Initialize the Gemini 2.5 Flash model
# It will automatically look for the GOOGLE_API_KEY environment variable
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# Define the node function that calls the model
def chatbot(state: State):
    response = llm.invoke(state["messages"])
    # We return a dictionary because this will be merged into the state
    return {"messages": [response]}

# Create the graph builder
graph_builder = StateGraph(State)

# Add our node to the graph
graph_builder.add_node("chatbot", chatbot)

# Define the edges (the flow of the graph)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

# Compile the graph into an executable runnable
agent = graph_builder.compile()

if __name__ == "__main__":
    print("LangGraph Agent with Gemini 2.5 Flash initialized.")
    
    # Check if the API key is set to run a quick test
    if "GOOGLE_API_KEY" in os.environ:
        print("-" * 50)
        user_input = "Hi there! What can you tell me about the Gemini 2.5 Flash model?"
        print(f"User: {user_input}\n")
        
        # We invoke the agent with an initial state containing the user's message
        initial_state = {"messages": [HumanMessage(content=user_input)]}
        
        # Use stream_mode="values" to yield the entire state after each node runs
        for event in agent.stream(initial_state, stream_mode="values"):
            # The last message in the state is the most recent one
            event["messages"][-1].pretty_print()
    else:
        print("Please set the GOOGLE_API_KEY environment variable to test the agent.")
        print('Example: export GOOGLE_API_KEY="your_api_key_here"')
