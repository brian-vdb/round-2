// pages/components/Chat.tsx

import React, { useState, useCallback, useRef, useEffect, useLayoutEffect } from "react";
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
  const [identity, setIdentity] = useState<string | null>(null);
  const socketRef = useRef<WebSocket | null>(null);
  const isAtBottomRef = useRef(true);
  const containerRef = useRef<HTMLDivElement>(null);

  // auto-scroll when messages change, only if user was at bottom
  useLayoutEffect(() => {
    if (isAtBottomRef.current && containerRef.current) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight;
    }
  }, [messages]);

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
      const token = localStorage.getItem('authToken');
      const params = token ? `?token=${encodeURIComponent(token)}` : '';
      const socket = new WebSocket(`${WS_URL}${params}`);
      socketRef.current = socket;

      socket.onopen = () => {
        socket.send(text);
      };

      socket.onmessage = (event: MessageEvent) => {
        try {
          const data: Message = JSON.parse(event.data);
          if (data.identity !== identity) {
            setIdentity(data.identity);
            addMessage({ identity: 'new-identity', message: `You are now chatting with the ${data.identity} agent` });
          }
          addMessage(data);
        } catch {
          console.error('Invalid message format');
        }
      };

      socket.onclose = () => {
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

  /**
   * Handle scroll events in the messages container.
   */
  const handleScroll = useCallback(() => {
    if (!containerRef.current) return;
    const { scrollTop, scrollHeight, clientHeight } = containerRef.current;
    // within 20px of bottom => consider at bottom
    isAtBottomRef.current = scrollHeight - scrollTop <= clientHeight + 20;
  }, []);

  return { messages, addMessage, sendMessage, containerRef, handleScroll };
}

/**
 * Chat component with slide-up panel, message list, and input form.
 */
const Chat: React.FC = () => {
  const [open, setOpen] = useState(false);
  const [input, setInput] = useState("");
  const { messages, addMessage, sendMessage, containerRef, handleScroll } = useChatWebSocket();

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    const text = input.trim();
    if (!text) return;

    addMessage({ identity: 'user', message: text });
    sendMessage(text);
    setInput("");

    if (containerRef.current) {
      setTimeout(() => {
        containerRef.current!.scrollTop = containerRef.current!.scrollHeight;
      }, 0);
    }
  };

  return (
    <div className={`chat ${open ? 'open' : 'closed'}`}>
      <div className="header" onClick={() => setOpen(o => !o)}>
        <h2 className="title">Customer Support</h2>
        <div className="status-icon" />
      </div>
      <div className="content">
        <div
          className="messages"
          ref={containerRef}
          onScroll={handleScroll}
        >
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`message ${msg.identity}`}>
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
