// pages/Information.tsx

import React, { useState, useEffect } from 'react';
import './Information.css';

// Data interface for FAQ items
export interface FaqItemData {
  question: string;
  answer: string;
}

// Payload interface for the full information page
interface InformationPage {
  faq: FaqItemData[];
}

// Define the API base URL
const API_URL = 'http://127.0.0.1:8000';

// Function to fetch the full information payload from the API
export const fetchInformation = async (): Promise<InformationPage> => {
  const response = await fetch(`${API_URL}/information`);
  if (!response.ok) {
    throw new Error(`Server error: ${response.status}`);
  }
  const data: InformationPage = await response.json();
  return data;
};

// Presentational component for a single FAQ item
const FaqItem: React.FC<FaqItemData> = ({ question, answer }) => (
  <div className='faq-item'>
    <h2 className='question'>{question}</h2>
    <p className='answer'>{answer}</p>
  </div>
);

const Information: React.FC = () => {
  const [faqItems, setFaqItems] = useState<FaqItemData[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const loadInformation = async () => {
      try {
        const page = await fetchInformation();
        setFaqItems(page.faq);
      } finally {
        setLoading(false);
      }
    };

    loadInformation();
  }, []);

  if (loading) {
    return (
      <></>
    );
  }

  return (
    <main className='page about-page'>
      <h1 className='title'>Frequently Asked Questions</h1>
      <div className='faq-form'>
        {faqItems.map((item, index) => (
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
