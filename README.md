# Round 2

A brief description of your project.

## Table of Contents

- [Round 2](#round-2)
  - [Table of Contents](#table-of-contents)
  - [About](#about)
  - [Features](#features)
  - [Architecture](#architecture)
  - [Tech Stack](#tech-stack)
    - [Frontend](#frontend)
    - [Backend API](#backend-api)
    - [Database](#database)
    - [Authentication](#authentication)
    - [AI Integration](#ai-integration)
  - [Configuration](#configuration)
  - [Usage](#usage)

## About

This project is a full-stack web application that leverages modern technologies to test my capabilities with AI-driven features. The frontend is built in React, while the backend API is developed using FastAPI in Python. MongoDB serves as the vector database for semantic search, and security is handled with JWT tokens and Argon2 password hashing. AI capabilities are integrated via OpenAI models through LangGraph.

## Features

* **Interactive React Frontend**: Responsive UI for end users.
* **FastAPI Backend**: High-performance asynchronous API in Python.
* **Semantic Search**: Vector search powered by MongoDB to allow RAG.
* **Secure Authentication**: JWT for stateless auth, Argon2 for secure password hashing.
* **AI-Powered Intelligence**: OpenAI models accessed through LangGraph:

  * **Action Model**: `gpt-4o-mini` for decision-making and process automation.
  * **Information Model**: `gpt-4o` for information retrieval and content generation.

## Architecture

```plaintext
+----------------+    HTTP    +----------------+    MongoDB    +-------------+
|                | <--------> |                | -----------> |              |
| React Frontend |            | FastAPI Backend|              | MongoDB Atlas|
|                | <--------> |                | -----------> | Vector Store |
+----------------+ WebSockets +----------------+              +-------------+
                                   ^
                                   | OpenAI (GPT via LangGraph)
                                   v
                          +-----------------------------+
                          |  Action & Information Models|
                          +-----------------------------+
```

## Tech Stack

### Frontend

* **React**: Component-based UI library.
* **TypeScript** (optional): For type safety and better developer experience.
* **CSS-in-JS / Tailwind** (optional): Styling solutions.

### Backend API

* **FastAPI**: Modern, fast (high-performance) web framework for building APIs with Python 3.7+.
* **Pydantic**: Data validation and settings management.
* **Uvicorn**: ASGI server for serving the app.

### Database

* **MongoDB**:

  * Used as a vector database for semantic search implementation.
  * Stores embeddings for documents and queries.
  * Supports fast approximate nearest neighbor search.

### Authentication

* **JWT (JSON Web Tokens)**: Stateless token-based authentication.
* **Argon2**: Password hashing algorithm for secure storage of user credentials.

### AI Integration

* **LangGraph**: Orchestrates interactions with OpenAI models.
* **OpenAI**:

  * **Action Model (`gpt-4o-mini`)**: Handles logic, routing, and automated tasks.
  * **Information Model (`gpt-4o`)**: Responsible for content generation, summarization, and info retrieval.

## Configuration

1. **Environment Variables**

   * Create a `.env` file in the `backend` directory based on the `.env.template`:

## Usage

1. **Run Backend**

   ```bash
   cd backend
   python app.py
   ```

2. **Run Frontend**

   ```bash
   cd frontend
   npm run dev
   ```

3. **Access the App**

   * Navigate to `http://localhost:3000` in your browser.
