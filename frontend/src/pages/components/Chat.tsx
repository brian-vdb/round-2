// pages/components/Chat.tsx

import React, { useState, useCallback, useEffect } from "react";
import type { FormEvent } from "react";
import './Chat.css';

/**
 * Represents a chat message with an identity and content.
 */
export interface Message {
  identity: string;
  message: string;
}

const WS_URL = 'ws://127.0.0.1:8000/chat/ws';

/**
 * Custom hook to manage a persistent chat WebSocket connection.
 */
export function useChatWebSocket() {
  const [messages, setMessages] = useState<Message[]>([]);
  const socketRef = React.useRef<WebSocket | null>(null);

  /**
   * Append a message to the local message list.
   */
  const addMessage = useCallback((msg: Message) => {
    setMessages(prev => [...prev, msg]);
  }, []);

  /**
   * Send text to the server via WebSocket (opens connection if needed).
   */
  const sendMessage = useCallback((text: string) => {
    if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
      socketRef.current.send(text);
    } else {
      const token = localStorage.getItem('token');
      const params = token ? `?token=${encodeURIComponent(token)}` : '';
      const socket = new WebSocket(`${WS_URL}${params}`);
      socketRef.current = socket;

      socket.onopen = () => {
        console.log('WebSocket connected');
        socket.send(text);
      };

      socket.onmessage = (event: MessageEvent) => {
        try {
          const data: Message = JSON.parse(event.data);
          addMessage(data);
        } catch {
          console.error('Invalid message format');
        }
      };

      socket.onclose = () => {
        console.log('WebSocket disconnected');
        socketRef.current = null;
      };

      socket.onerror = (err) => {
        console.error('WebSocket error', err);
      };
    }
  }, [addMessage]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      socketRef.current?.close();
    };
  }, []);

  return { messages, addMessage, sendMessage };
}

const Chat: React.FC = () => {
  const [open, setOpen] = useState(false);
  const [input, setInput] = useState("");
  const { messages, addMessage, sendMessage } = useChatWebSocket();

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    const text = input.trim();
    if (!text) return;

    // Append user message locally
    addMessage({ identity: 'user', message: text });

    // Send to server
    sendMessage(text);
    setInput("");
  };

  return (
    <div className={`chat ${open ? 'open' : 'closed'}`}>
      <div className="header" onClick={() => setOpen(o => !o)}>
        <h2 className="title">Customer Support</h2>
        <div className="status-icon" />
      </div>
      <div className="content">
        <div className="messages">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`message ${msg.identity === 'user' ? 'from-user' : 'from-bot'}`}>
              <span className="identity">{msg.identity}:</span>
              <span className="text">{msg.message}</span>
            </div>
          ))}
        </div>
        <form onSubmit={handleSubmit} className="input-form">
          <input
            type="text"
            value={input}
            onChange={e => setInput(e.target.value)}
            placeholder="Type your message…"
            className="input"
          />
          <button type="submit" className="send-button">Send</button>
        </form>
      </div>
    </div>
  );
};

export default Chat;
