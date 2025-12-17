// Simple test to verify the chatbot component can be imported and used
import React from 'react';
import { render, screen } from '@testing-library/react';
import ChatbotWidget from './ChatbotWidget';

// Mock the API service
jest.mock('../services/chatbotAPI', () => ({
  askQuestion: jest.fn()
}));

describe('ChatbotWidget', () => {
  test('renders without crashing', () => {
    render(<ChatbotWidget />);
    // The chatbot button should be present
    const chatbotButton = screen.getByRole('button');
    expect(chatbotButton).toBeInTheDocument();
  });

  test('initially shows closed state', () => {
    render(<ChatbotWidget />);
    // The modal should not be visible initially
    const modal = screen.queryByRole('dialog');
    expect(modal).not.toBeInTheDocument();
  });
});