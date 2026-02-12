import React from 'react';
import ChatbotWidget from '../components/ChatbotWidget';

const ChatbotPage = () => {
  return (
    <div className="textbook-container">
      <div className="container">
        <div className="row">
          <div className="col col--12">
            <h1>AI Textbook Assistant</h1>
            <p>
              Welcome to the AI-powered textbook assistant. Ask questions about the Physical AI textbook,
              and I'll provide answers with citations to the source material.
            </p>

            <div style={{
              marginTop: '2rem',
              padding: '1rem',
              backgroundColor: '#f8f9fa',
              borderRadius: '8px',
              minHeight: '400px'
            }}>
              <ChatbotWidget />
              <p style={{ marginTop: '2rem' }}>
                You can also use the floating chatbot button on any page to ask questions about the textbook content.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatbotPage;