import { useState, useRef, useEffect } from 'react';
import axios from 'axios';

const ChatInterface = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

  // Auto-scroll to bottom when new messages arrive
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { 
      type: 'user', 
      text: input,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await axios.post(`${API_URL}/query`, {
        message: input
      }, {
        timeout: 30000 // 30 second timeout
      });

      const botMessage = { 
        type: 'bot', 
        text: response.data.response,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error:', error);
      
      let errorText = 'Sorry, I encountered an error. Please try again.';
      
      if (error.code === 'ECONNABORTED') {
        errorText = 'Request timed out. Please try again with a simpler question.';
      } else if (error.response) {
        errorText = `Error: ${error.response.data.detail || 'Server error'}`;
      } else if (error.request) {
        errorText = 'Cannot connect to the server. Please make sure the backend is running.';
      }
      
      const errorMessage = { 
        type: 'bot', 
        text: errorText,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        isError: true
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const clearChat = () => {
    setMessages([]);
  };

  const exampleQuestions = [
    "What is quantum computing?",
    "Explain photosynthesis",
    "What's the weather in Pune?",
    "Calculate 234 * 567",
    "Write a haiku about AI",
    "How does blockchain work?"
  ];

  const handleExampleClick = (question) => {
    setInput(question);
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <div className="header-content">
          <h1>🤖 AI Chat Assistant</h1>
          <p>Ask me anything! I can help with explanations, calculations, weather, and more.</p>
        </div>
        {messages.length > 0 && (
          <button className="clear-btn" onClick={clearChat} title="Clear chat">
            🗑️ Clear
          </button>
        )}
      </div>

      <div className="messages-container">
        {messages.length === 0 && (
          <div className="welcome-message">
            <div className="welcome-icon">💬</div>
            <h2>Welcome to AI Chat Assistant!</h2>
            <p>I'm here to help you with anything you need. Try asking me about:</p>
            
            <div className="capabilities">
              <div className="capability-item">
                <span className="icon">📚</span>
                <span>General Knowledge</span>
              </div>
              <div className="capability-item">
                <span className="icon">💻</span>
                <span>Technology & Coding</span>
              </div>
              <div className="capability-item">
                <span className="icon">🔬</span>
                <span>Science & Math</span>
              </div>
              <div className="capability-item">
                <span className="icon">🌤️</span>
                <span>Weather Information</span>
              </div>
              <div className="capability-item">
                <span className="icon">🧮</span>
                <span>Calculations</span>
              </div>
              <div className="capability-item">
                <span className="icon">✍️</span>
                <span>Creative Writing</span>
              </div>
            </div>

            <div className="example-questions">
              <p className="example-title">Try these examples:</p>
              <div className="example-grid">
                {exampleQuestions.map((question, index) => (
                  <button
                    key={index}
                    className="example-btn"
                    onClick={() => handleExampleClick(question)}
                  >
                    {question}
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}
        
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.type} ${msg.isError ? 'error' : ''}`}>
            <div className="message-avatar">
              {msg.type === 'user' ? '👤' : '🤖'}
            </div>
            <div className="message-bubble">
              <div className="message-content">{msg.text}</div>
              <div className="message-time">{msg.timestamp}</div>
            </div>
          </div>
        ))}
        
        {loading && (
          <div className="message bot">
            <div className="message-avatar">🤖</div>
            <div className="message-bubble">
              <div className="message-content loading">
                <span className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </span>
                <span className="loading-text">Thinking...</span>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      <div className="input-container">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask me anything..."
          disabled={loading}
          rows="1"
        />
        <button 
          onClick={handleSend} 
          disabled={loading || !input.trim()}
          className="send-btn"
        >
          {loading ? '⏳' : '📤'}
        </button>
      </div>
    </div>
  );
};

export default ChatInterface;