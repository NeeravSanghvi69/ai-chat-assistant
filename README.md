AI Chat Assistant - SanchAI Analytics Technical Assessment

A full-stack AI-powered chat application that can answer questions on ANY topic using LangChain and OpenRouter.

Features

Core Capabilities
- General-Purpose AI Assistant: Answer questions on virtually any topic
- Natural Language Understanding: Powered by LangChain + OpenRouter LLM
- Tool Integration: Weather information and calculations
- Knowledge Domains: 
  - General Knowledge (History, Geography, Culture)
  - Technology & Programming
  - Science & Mathematics
  - Creative Writing & Arts
  - Problem Solving & Logic
  - And much more!

Technical Features
- Real-time chat interface
- Modern, responsive UI
- Async processing for better performance
- Comprehensive error handling
- Mobile-friendly design
- Message history in session

Tech Stack

Backend
- Framework: FastAPI
- AI/ML: LangChain, OpenRouter (Meta Llama 3.1)
- Tools: Weather API, Custom Calculator
- Language: Python 3.8+

Frontend
- Framework: React 18
- Build Tool: Vite
- HTTP Client: Axios
- Styling: CSS3 with modern features

Prerequisites

Before you begin, ensure you have:

- Python 3.8 or higher installed
- Node.js 16 or higher and npm
- Git for version control
- An OpenRouter API account (free tier available)
- (Optional) OpenWeatherMap API key for weather features

Installation & Setup

1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-chat-assistant.git
cd ai-chat-assistant
```

 2. Backend Setup

```bash
  Navigate to backend directory
cd backend

  Create and activate virtual environment
python -m venv venv

  On Windows:
venv\Scripts\activate

  On Mac/Linux:
source venv/bin/activate

  Install dependencies
pip install -r requirements.txt

  Create .env file
cp .env.example .env
  Or manually create .env with:
  OPENAI_API_KEY=your_openrouter_api_key_here
  OPENWEATHER_API_KEY=your_openweather_api_key_here (optional)
```

3. Frontend Setup

```bash
  Navigate to frontend directory (from root)
cd frontend

  Install dependencies
npm install

  Create .env file
echo "VITE_API_URL=http://localhost:8000" > .env
```

4. Get API Keys

OpenRouter API Key (Required)
1. Visit [OpenRouter.ai](https://openrouter.ai/)
2. Sign up for a free account
3. Navigate to Keys section
4. Generate a new API key
5. Add it to `backend/.env`:
   ```
   OPENAI_API_KEY=your_actual_key_here
   ```

OpenWeatherMap API Key (Optional)
1. Visit [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up for a free account
3. Generate an API key
4. Add it to `backend/.env`:

```
OPENWEATHER_API_KEY=your_actual_key_here
```

Running the Application

Start the Backend Server

```bash
cd backend
source venv/bin/activate    or venv\Scripts\activate on Windows
uvicorn app.main:app --reload --port 8000
```

The backend will be available at: `http://localhost:8000`

Start the Frontend Development Server

Open a new terminal:

```bash
cd frontend
npm run dev
```

The frontend will be available at: `http://localhost:5173`

Verify Installation

1. Backend: Visit `http://localhost:8000` - should show API info
2. Frontend: Visit `http://localhost:5173` - should show chat interface
3. Try sending a message like "What is artificial intelligence?"

Usage Examples

General Questions
```
User: What is quantum computing?
AI: [Provides detailed explanation of quantum computing concepts]

User: Explain photosynthesis
AI: [Explains the process of photosynthesis step by step]
```

 Weather Queries (if API configured)
```
User: What's the weather in Pune?
AI: Current weather in Pune:
    🌡️ Temperature: 24°C (feels like 23°C)
    ☁️ Conditions: Clear sky
    💧 Humidity: 45%
    💨 Wind Speed: 3.5 m/s
```

Calculations
```
User: Calculate 234  567
AI: The result of 234  567 is 132678
```

Creative Tasks
```
User: Write a haiku about technology
AI: [Creates an original haiku]
```

API Endpoints

Main Endpoints

`POST /query`
Process user queries and get AI responses

Request:
```json
{
  "message": "What is machine learning?"
}
```

Response:
```json
{
  "response": "Machine learning is a subset of artificial intelligence..."
}
```

`GET /health`
Check API health status

Response:
```json
{
  "status": "healthy",
  "service": "AI Chat Assistant",
  "api_version": "1.0.0"
}
```

`GET /info`
Get information about assistant capabilities

Response:
```json
{
  "name": "AI Chat Assistant",
  "capabilities": [...],
  "example_queries": [...]
}
```

Project Structure

```
ai-chat-assistant/
├── backend/
│   ├── app/
│   │   ├── __init__.py            Package initialization
│   │   ├── main.py                FastAPI application & endpoints
│   │   ├── agent.py               LangChain agent configuration
│   │   └── tools.py               Custom tools (weather, calculator)
│   ├── requirements.txt           Python dependencies
│   └── .env                       Environment variables (not in repo)
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── ChatInterface.jsx    Main chat component
│   │   ├── App.jsx                Root component
│   │   ├── App.css                Styles
│   │   └── main.jsx               Entry point
│   ├── package.json               Node dependencies
│   └── .env                       Frontend environment variables
├── README.md                      This file
└── .gitignore                     Git ignore rules
```

   🛠️ Architecture

    Action Flow

1. User Input: User types a message in the chat interface
2. Frontend Processing: React component captures input and sends POST request
3. Backend Reception: FastAPI endpoint receives the query
4. Agent Processing: LangChain agent analyzes the query
5. Tool Selection: Agent decides if tools (weather, calculator) are needed
6. LLM Interaction: Query processed by OpenRouter (Meta Llama 3.1)
7. Response Generation: AI generates appropriate response
8. Response Return: Backend sends response back to frontend
9. Display: Frontend displays the AI response in chat


Key Components

Backend Components
- FastAPI Server: Handles HTTP requests and CORS
- LangChain Agent: Orchestrates LLM and tool usage
- OpenRouter LLM: Provides language understanding and generation
- Custom Tools: Weather API integration, calculator

Frontend Components
- ChatInterface: Main chat UI component
- Message Display: Renders user and AI messages
- Input Handler: Captures and sends user input
- State Management: React hooks for messages and loading states

Testing

Manual Testing

Test the following scenarios:

1. General Knowledge
   - "What is the capital of Japan?"
   - "Explain the water cycle"

2. Technology
   - "What is machine learning?"
   - "How does the internet work?"

3. Science
   - "What causes earthquakes?"
   - "Explain Newton's laws"

4. Math
   - "Calculate 15  89 + 234"
   - "What is 20% of 450?"

5. Weather (if configured)
   - "What's the weather in London?"
   - "Tell me the weather in Tokyo"

6. Creative
   - "Write a short poem"
   - "Give me a joke"

Testing with curl

```bash
  Test general question
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"message": "What is artificial intelligence?"}'

  Test weather
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the weather in Pune?"}'

  Test calculation
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"message": "Calculate 123  456"}'
```

Troubleshooting

Common Issues

 Backend Issues

Problem: "Module not found" error
```bash
Solution: Ensure virtual environment is activated and dependencies are installed
pip install -r requirements.txt
```

Problem: "API key not found" error
```bash
Solution: Check .env file has correct API keys
Make sure .env is in backend/ directory
```

Problem: Port 8000 already in use
```bash
Solution: Use a different port
uvicorn app.main:app --reload --port 8001
  Update VITE_API_URL in frontend/.env accordingly
```

Frontend Issues

Problem: "Cannot connect to server"
```bash
Solution: 
1. Verify backend is running on http://localhost:8000
2. Check VITE_API_URL in frontend/.env
3. Ensure CORS is properly configured
```

Problem: Build errors
```bash
Solution: Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

    Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| Connection refused | Backend not running | Start backend server |
| 401 Unauthorized | Invalid API key | Check OpenRouter API key |
| 500 Internal Server Error | Backend error | Check backend logs |
| Timeout | Slow response | Increase timeout or simplify query |

Security Considerations

- API keys are stored in `.env` files (not committed to repo)
- CORS is configured to allow only specific origins
- Input validation on backend
- Error messages don't expose sensitive information
- Rate limiting can be added for production use

Deployment

Backend Deployment (Example with Heroku)

```bash
  Install Heroku CLI and login
heroku login

  Create Heroku app
heroku create your-app-name

  Set environment variables
heroku config:set OPENROUTER_API_KEY=your_key

  Deploy
git push heroku main
```

Frontend Deployment (Example with Vercel)

```bash
  Install Vercel CLI
npm i -g vercel

  Deploy
cd frontend
vercel

  Set environment variable
  VITE_API_URL=https://your-backend-url.herokuapp.com
```

Development Notes

Adding New Tools

To add a new tool to the agent:

1. Create the tool function in `backend/app/tools.py`:
```python
@tool
def your_new_tool(param: str) -> str:
    """Tool description"""
      Implementation
    return result
```

2. Add to tools list in `backend/app/agent.py`:
```python
tools = [get_weather, calculate, your_new_tool]
```

Customizing the LLM

To use a different model:

```python
  In backend/app/agent.py
llm = ChatOpenAI(
    model="your-preferred-model",    Change model here
    openai_api_key=OPENROUTER_API_KEY,
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0.7,
)
```


Neerav Sanghvi
- GitHub: [@NeeravSanghvi69](https://github.com/NeeravSanghvi69)



Support

For issues or questions:
1. Check the troubleshooting section
2. Review backend logs: check terminal running uvicorn
3. Review frontend console: open browser DevTools (F12)
4. Ensure all environment variables are set correctly

---

