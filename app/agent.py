# backend/app/agent.py

import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

from app.tools import get_weather, calculate

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Try a more capable model for better tool usage
# Option 1: GPT-4 Turbo (best, but costs more)
# Option 2: GPT-3.5 Turbo (good balance)
# Option 3: Llama 3.1 70B (better than 8B for tool calling)

llm = ChatOpenAI(
    model="openai/gpt-3.5-turbo",  # Changed to GPT-3.5 for better tool calling
    openai_api_key=OPENAI_API_KEY,
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0.7,
    max_tokens=1500,
)

# Alternative models you can try:
# model="openai/gpt-4-turbo"  # Best quality
# model="meta-llama/llama-3.1-70b-instruct"  # Better Llama
# model="anthropic/claude-3-haiku"  # Fast and good

# Define tools
tools = [get_weather, calculate]

# Improved prompt that forces tool usage
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a helpful AI assistant with access to real-time tools.

CRITICAL INSTRUCTIONS:
1. For weather queries: ALWAYS call get_weather tool first, then respond with the weather data
2. For calculation queries: ALWAYS call calculate tool first, then respond with the result
3. NEVER say you cannot access real-time data - you CAN via tools
4. After calling a tool, YOU MUST use its output in your final response

Available Tools:
- get_weather(city): Returns current weather - REQUIRED for any weather question
- calculate(expression): Returns calculation result - REQUIRED for any math question

Example flows:
User: "What's the weather in London?"
→ Call get_weather("London")
→ Respond: "Here's the current weather in London: [tool output]"

User: "Calculate 15 * 23"
→ Call calculate("15 * 23")
→ Respond: "The calculation result is: [tool output]"

For other questions, answer directly using your knowledge."""),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# Create agent
agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)

# Agent executor
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=5,
    early_stopping_method="force",
    return_intermediate_steps=False
)

async def process_query(user_query: str) -> str:
    """
    Process any user query through the LangChain agent
    """
    try:
        result = await agent_executor.ainvoke({"input": user_query})
        
        # Extract output
        if isinstance(result, dict) and "output" in result:
            output = result["output"]
            if output and output.strip():
                return str(output)
        
        return "I apologize, but I couldn't generate a proper response. Please try again."

    except Exception as e:
        print(f"Error processing query: {str(e)}")
        import traceback
        traceback.print_exc()
        return "I apologize, but I encountered an error. Please try again."