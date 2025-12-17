import React from 'react';
import { AuthProvider } from '../contexts/AuthContext';
import ChatbotWidget from '../components/ChatbotWidget';

// Default theme Root component
import OriginalRoot from '@theme-original/Root';

export default function Root(props) {
  return (
    <OriginalRoot {...props}>
      <AuthProvider>
        {props.children}
        <ChatbotWidget />
      </AuthProvider>
    </OriginalRoot>
  );
}