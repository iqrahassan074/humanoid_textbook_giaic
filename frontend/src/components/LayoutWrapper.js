import React from 'react';
import { AuthProvider } from '../contexts/AuthContext';
import ChatbotWidget from './ChatbotWidget';

const LayoutWrapper = ({ children }) => {
  return (
    <AuthProvider>
      {children}
      <ChatbotWidget />
    </AuthProvider>
  );
};

export default LayoutWrapper;