import React, { useState, useEffect, useRef } from 'react';
import chatbotAPI from '../services/chatbotAPI';
import './ChatbotWidget.css';

const ChatbotWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const messagesEndRef = useRef(null);

  // Scroll to bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Handle sending a message
  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      text: inputValue,
      sender: 'user',
      timestamp: new Date()
    };

    // Add user message to chat
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);
    setError(null);

    try {
      // Call the backend API
      const response = await chatbotAPI.askQuestion(inputValue);

      const botMessage = {
        id: Date.now() + 1,
        text: response.answer,
        sender: 'bot',
        citations: response.citations,
        confidence: response.confidence_score,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error getting response from chatbot:', error);
      setError('Sorry, I encountered an error processing your question. Please try again.');

      const errorMessage = {
        id: Date.now() + 1,
        text: 'Sorry, I encountered an error processing your question. Please try again.',
        sender: 'bot',
        timestamp: new Date()
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  // Handle Enter key press
  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  // Toggle chatbot open/close
  const toggleChatbot = () => {
    setIsOpen(!isOpen);
  };

  // Clear chat
  const clearChat = () => {
    setMessages([]);
    setError(null);
  };

  return (
    <div className="chatbot-container">
      {isOpen && (
        <div className="chatbot-modal">
          <div className="chatbot-header">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <h3>AI Textbook Assistant</h3>
              <button
                onClick={clearChat}
                style={{
                  background: 'none',
                  border: 'none',
                  color: 'white',
                  cursor: 'pointer',
                  fontSize: '1rem'
                }}
              >
                Clear
              </button>
            </div>
          </div>
          <div className="chatbot-body">
            {messages.length === 0 ? (
              <div className="welcome-message">
                <p>Hello! I'm your AI textbook assistant. Ask me anything about the Physical AI textbook, and I'll provide answers with citations to the source material.</p>
                <p>Try asking: "What is Physical AI?" or "Explain sensorimotor learning"</p>
              </div>
            ) : (
              <div className="messages-container">
                {messages.map((message) => (
                  <div
                    key={message.id}
                    className={`message ${message.sender}-message`}
                  >
                    <div className="message-text">{message.text}</div>
                    {message.sender === 'bot' && message.citations && message.citations.length > 0 && (
                      <div className="citations">
                        <strong>Citations:</strong>
                        <ul>
                          {message.citations.map((citation, index) => (
                            <li key={index}>
                              Chapter: {citation.chapter}, Section: {citation.section}
                              {citation.similarity_score && (
                                <span> (Relevance: {(citation.similarity_score * 100).toFixed(1)}%)</span>
                              )}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                    {message.sender === 'bot' && message.confidence && (
                      <div className="confidence">
                        Confidence: {(message.confidence * 100).toFixed(1)}%
                      </div>
                    )}
                  </div>
                ))}
                {isLoading && (
                  <div className="message bot-message">
                    <div className="typing-indicator">
                      AI is thinking...
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>
            )}
            {error && (
              <div className="error-message">
                {error}
              </div>
            )}
          </div>
          <div className="chatbot-footer">
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask a question about the textbook..."
              className="chat-input"
              disabled={isLoading}
            />
            <button
              onClick={handleSendMessage}
              className="chat-send-button"
              disabled={isLoading || !inputValue.trim()}
            >
              Send
            </button>
          </div>
        </div>
      )}
      <button
        className="chatbot-button"
        onClick={toggleChatbot}
      >
        {isOpen ? '×' : '💬'}
      </button>
    </div>
  );
};

export default ChatbotWidget;