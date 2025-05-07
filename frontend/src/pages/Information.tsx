// pages/Information.tsx

import React, { useState, useEffect } from 'react';
import './Information.css';

// Data interface for FAQ items
export interface FAQItemData {
  question: string;
  answer: string;
}

// Define the API URL
const API_URL = 'http://127.0.0.1:8000';

// Function to fetch the FAQ list from the API
export const fetchInformation = async (): Promise<FAQItemData[]> => {
  const response = await fetch(`${API_URL}/information/faq`);
  if (!response.ok) {
    throw new Error(`Server error: ${response.status}`);
  }
  const data: FAQItemData[] = await response.json();
  return data;
};

// Presentational component for a single FAQ item
const FaqItem: React.FC<FAQItemData> = ({ question, answer }) => (
  <div className='faq-item'>
    <h2 className='question'>{question}</h2>
    <p className='answer'>{answer}</p>
  </div>
);

const Information: React.FC = () => {
  const [items, setItems] = useState<FAQItemData[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const loadItems = async () => {
      try {
        const data = await fetchInformation();
        setItems(data);
      } finally {
        setLoading(false);
      }
    };

    loadItems();
  }, []);

  if (loading) {
    return (
      <main className='page about-page'>
        <h1 className='title'>Frequently Asked Questions</h1>
        <p>Loading...</p>
      </main>
    );
  }

  return (
    <main className='page about-page'>
      <h1 className='title'>Frequently Asked Questions</h1>
      <div className='faq-form'>
        {items.map((item, index) => (
          <FaqItem
            key={index}
            question={item.question}
            answer={item.answer}
          />
        ))}
      </div>
    </main>
  );
};

export default Information;
