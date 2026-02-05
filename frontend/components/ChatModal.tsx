import React, { useState, useEffect, useRef } from 'react';
import { X, Send, Loader2 } from 'lucide-react';
import { chatAPI, apiClient } from '../lib/api';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

interface ChatModalProps {
  isOpen: boolean;
  onClose: () => void;
  conversationId?: number | null;
  onTaskUpdate?: () => void; // Callback to notify parent when tasks are modified
}

const ChatModal: React.FC<ChatModalProps> = ({ isOpen, onClose, conversationId: initialConversationId, onTaskUpdate }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<number | null>(initialConversationId ?? null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Initialize conversation when modal opens with an existing conversation
  useEffect(() => {
    if (isOpen && initialConversationId) {
      // If we have an initial conversation ID, initialize with it
      setConversationId(initialConversationId);
      // Load conversation history from backend
      const loadConversationHistory = async () => {
        try {
          // Use the API client to fetch messages
          const apiMessages = await apiClient.getConversationHistory(initialConversationId);
          const formattedMessages: Message[] = apiMessages.map((msg: any) => ({
            id: msg.id.toString(),
            role: msg.role,
            content: msg.content,
            timestamp: new Date(msg.timestamp),
          }));
          setMessages(formattedMessages);
        } catch (error) {
          console.error('Error loading conversation history:', error);
          setMessages([]); // Start with empty messages on error
        }
      };

      loadConversationHistory();
    } else if (isOpen && !initialConversationId) {
      // New conversation
      setConversationId(null);
      setMessages([]); // Only clear messages for new conversations
    }
  }, [isOpen, initialConversationId]);

  // Scroll to bottom of messages
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSend = async () => {
    if (!inputValue.trim() || isLoading) return;

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputValue,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Call the chat API
      const response = await chatAPI(inputValue, conversationId);

      // Update conversation ID if it's a new conversation
      if (!conversationId) {
        setConversationId(response.conversation_id);
      }

      // Handle different actions from the chatbot
      switch (response.action) {
        case 'add':
          // The task was added, we could potentially update the task list here
          console.log('Task added:', response.task);
          // Notify parent component about the new task
          if (onTaskUpdate) onTaskUpdate();
          break;
        case 'delete':
          // The task was deleted, we could potentially update the task list here
          console.log('Task deleted:', response.task);
          // Notify parent component about the deleted task
          if (onTaskUpdate) onTaskUpdate();
          break;
        case 'update':
          // The task was updated, we could potentially update the task list here
          console.log('Task updated:', response.task);
          // Notify parent component about the updated task
          if (onTaskUpdate) onTaskUpdate();
          break;
        case 'complete':
          // The task was completed, we could potentially update the task list here
          console.log('Task completed:', response.task);
          // Notify parent component about the completed task
          if (onTaskUpdate) onTaskUpdate();
          break;
        case 'list':
          // The task list was requested, we could potentially update the task list here
          console.log('Task list requested');
          // Notify parent component to refresh the task list
          if (onTaskUpdate) onTaskUpdate();
          break;
        case 'none':
          // General conversation, no specific task action
          break;
        default:
          console.warn('Unknown action from chatbot:', response.action);
      }

      // Add assistant message - now using the message property from the new response format
      const assistantMessage: Message = {
        id: `assistant-${Date.now()}`,
        role: 'assistant',
        content: response.message,
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);

      // Add error message
      const errorMessage: Message = {
        id: `error-${Date.now()}`,
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-xl w-full max-w-md h-[600px] flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-gray-700">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white">AI Todo Assistant</h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
            aria-label="Close chat"
          >
            <X size={20} />
          </button>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.length === 0 ? (
            <div className="text-center text-gray-500 dark:text-gray-400 mt-8">
              <p>Hello! I'm your AI Todo assistant.</p>
              <p>Ask me to add, list, complete, or delete tasks.</p>
            </div>
          ) : (
            messages.map((message) => (
              <div
                key={message.id}
                className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                <div
                  className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                    message.role === 'user'
                      ? 'bg-blue-500 text-white'
                      : 'bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200'
                  }`}
                >
                  <p>{message.content}</p>
                  <p className={`text-xs mt-1 ${message.role === 'user' ? 'text-blue-200' : 'text-gray-500 dark:text-gray-400'}`}>
                    {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </p>
                </div>
              </div>
            ))
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="border-t border-gray-200 dark:border-gray-700 p-4">
          <div className="flex items-center">
            <textarea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Type your message..."
              className="flex-1 border border-gray-300 dark:border-gray-600 rounded-l-lg p-2 resize-none h-12 max-h-32 dark:bg-gray-700 dark:text-white"
              disabled={isLoading}
            />
            <button
              onClick={handleSend}
              disabled={isLoading || !inputValue.trim()}
              className={`bg-blue-500 text-white rounded-r-lg px-4 py-2 h-12 flex items-center ${
                isLoading || !inputValue.trim() ? 'opacity-50 cursor-not-allowed' : 'hover:bg-blue-600'
              }`}
              aria-label="Send message"
            >
              {isLoading ? (
                <Loader2 className="h-5 w-5 animate-spin" />
              ) : (
                <Send size={18} />
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatModal;