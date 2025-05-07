import React from 'react';
import './Index.css';

const Index: React.FC = () => {
  return (
    <main className="page index-page">
      {/* Hero Section */}
      <section className="hero">
        <div className="hero-content">
          <h1>TCS Pace™ Innovation Hub</h1>
          <p className="tagline">
            Bringing the best of TCS innovation—explore emerging technologies and define your innovation strategy for better outcomes.
          </p>
        </div>
      </section>

      {/* Experience Section */}
      <section className="experience">
        <h2>Experience the Future</h2>
        <p>Go from standstill to sea change, and from today to tomorrow, at speed and scale with TCS Pace™.</p>
      </section>

      {/* Set the Pace */}
      <section className="set-pace">
        <h2>Set the Pace of Your Innovation Journey</h2>
        <p>
          Welcome to a platform that brings together the best of TCS capabilities in innovation to
          create meaningful impact. Tap into a collective intelligence of start-ups, developers,
          design thinkers, and academia to refine your strategy.
        </p>
      </section>
    </main>
  );
};

export default Index;
