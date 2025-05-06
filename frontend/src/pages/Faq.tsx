import { useState, useEffect } from 'react';

// Data interface for FAQ items
interface FAQItemData {
  question: string;
  answer: string;
}

// Presentational component for a single FAQ item
function FaqItem({ question, answer }: FAQItemData) {
  return (
    <div className='faq-item'>
      <h2 className='question'>{question}</h2>
      <p className='answer'>{answer}</p>
    </div>
  );
}

export default function Faq() {
  const [items, setItems] = useState<FAQItemData[]>([]);

  useEffect(() => {
    // TODO: replace placeholder with real API call
    const placeholder: FAQItemData[] = [
      { question: 'What is Vite?', answer: 'Vite is a fast build tool and dev server.' },
      { question: 'What is React Router?', answer: 'React Router is a library for routing in React apps.' }
    ];
    setItems(placeholder);
  }, []);

  return (
    <div className='page'>
      <h1 className='title'>FAQ</h1>
      <div className='faq-form'>
        {items.map((item, index) => (
          <FaqItem
            key={index}
            question={item.question}
            answer={item.answer}
          />
        ))}
      </div>
    </div>
  );
}
