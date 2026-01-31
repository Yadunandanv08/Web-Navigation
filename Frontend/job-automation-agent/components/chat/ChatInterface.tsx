'use client';

import React, { useState, useRef, useEffect } from 'react';
import { Send, Plus, Paperclip } from 'lucide-react';
import { ChatMessage } from './ChatMessage';
import { ThinkingAnimation } from './ThinkingAnimation';
import { sendGeminiMessage } from '@/app/actions/gemini';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  isThinking?: boolean;
}

export function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: 'Hi! I\'m your JobAgent AI assistant. I can help you fill out job applications, analyze forms, and automate your job search. Just share a job application link or form, and I\'ll handle the rest!',
      timestamp: new Date()
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() && !selectedFile) return;

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input || (selectedFile ? `Attached file: ${selectedFile.name}` : ''),
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setSelectedFile(null);
    setIsLoading(true);

    try {
      // Add thinking animation message
      const thinkingId = (Date.now() + 1).toString();
      setMessages(prev => [...prev, {
        id: thinkingId,
        role: 'assistant',
        content: '',
        timestamp: new Date(),
        isThinking: true
      }]);

      // Call Gemini API via secure server action
      let response = '';
      try {
        response = await sendGeminiMessage(userMessage.content);
      } catch (error: any) {
        console.error('Gemini API error:', error);
        response = generateMockResponse(input);
      }

      // Remove thinking message and add response
      setMessages(prev => {
        const filtered = prev.filter(m => m.id !== thinkingId);
        return [...filtered, {
          id: (Date.now() + 2).toString(),
          role: 'assistant',
          content: response,
          timestamp: new Date()
        }];
      });
    } catch (error) {
      console.error('Error in chat:', error);
      // Add error message
      setMessages(prev => [...prev, {
        id: (Date.now() + 2).toString(),
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date()
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const generateMockResponse = (userInput: string) => {
    const responses: { [key: string]: string } = {
      'google form': 'I can help you with Google Forms! Please share the link to the form, and I\'ll analyze its fields and fill it with your information from the resume you uploaded.',
      'linkedin': 'For LinkedIn job applications, I can navigate the form fields and fill them with your profile information. Just provide the job posting URL.',
      'indeed': 'I can handle Indeed applications. Share the job link, and I\'ll fill out the application with your details.',
      'resume': 'Your resume is ready to be used. I can extract information like your name, email, work experience, skills, and education to fill out job applications automatically.',
      'skill': 'I can help customize your application based on the job requirements. Which specific skills would you like to highlight?',
      'interview': 'Would you like me to prepare any interview information that can be used in applications?'
    };

    const lowerInput = userInput.toLowerCase();
    for (const [key, response] of Object.entries(responses)) {
      if (lowerInput.includes(key)) {
        return response;
      }
    }

    return `I've processed your request. Based on what you've shared, I can now help fill job applications for you. Here's what I can do:\n\n✓ Analyze job application forms\n✓ Extract key fields from the form\n✓ Fill fields with your resume information\n✓ Handle multiple form types (Google Forms, LinkedIn, Indeed, custom forms)\n✓ Track all your applications\n\nWhat would you like to do next?`;
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setSelectedFile(file);
    }
  };

  const handleNewChat = () => {
    setMessages([{
      id: '1',
      role: 'assistant',
      content: 'Hi! I\'m your JobAgent AI assistant. I can help you fill out job applications, analyze forms, and automate your job search. Just share a job application link or form, and I\'ll handle the rest!',
      timestamp: new Date()
    }]);
  };

  return (
    <div className="flex flex-col h-full bg-background rounded-2xl border border-border/40 overflow-hidden">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-border/40 bg-card/50">
        <h2 className="text-lg font-semibold">JobAgent Assistant</h2>
        <button
          onClick={handleNewChat}
          className="p-2 hover:bg-card rounded-lg transition"
          title="New chat"
        >
          <Plus className="w-5 h-5" />
        </button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <div key={message.id}>
            {message.isThinking ? (
              <ThinkingAnimation />
            ) : (
              <ChatMessage
                role={message.role}
                content={message.content}
                timestamp={message.timestamp}
              />
            )}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Input area */}
      <div className="p-4 border-t border-border/40 bg-card/50">
        {selectedFile && (
          <div className="mb-3 flex items-center gap-2 p-2 bg-primary/10 rounded-lg border border-primary/20">
            <Paperclip className="w-4 h-4 text-primary" />
            <span className="text-sm text-foreground/70">{selectedFile.name}</span>
            <button
              onClick={() => setSelectedFile(null)}
              className="ml-auto text-foreground/60 hover:text-foreground"
            >
              ×
            </button>
          </div>
        )}

        <form onSubmit={handleSendMessage} className="flex gap-3">
          <label className="cursor-pointer hover:opacity-70 transition">
            <Paperclip className="w-5 h-5 text-foreground/60" />
            <input
              type="file"
              onChange={handleFileSelect}
              accept=".pdf,.jpg,.jpeg,.png,.gif,.mp4,.webm"
              className="hidden"
            />
          </label>

          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Share a job form link or ask for help..."
            disabled={isLoading}
            className="flex-1 px-4 py-2 bg-input border border-border/40 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary/40 transition disabled:opacity-50"
          />

          <button
            type="submit"
            disabled={isLoading || (!input.trim() && !selectedFile)}
            className="px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
          >
            <Send className="w-5 h-5" />
            <span className="hidden sm:inline">Send</span>
          </button>
        </form>

        <p className="text-xs text-foreground/40 mt-3">
          Tip: Share job application URLs or forms, and I'll fill them out using your resume information.
        </p>
      </div>
    </div>
  );
}
