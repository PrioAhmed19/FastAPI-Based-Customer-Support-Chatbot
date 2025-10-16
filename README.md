# Product Chatbot REST API

A fully functional AI-powered chatbot REST API built with FastAPI that provides intelligent, human-like responses to customer queries about products using data from the DummyJSON Products API and Groq LLM.

## Features

- 🤖 **AI-Powered Chatbot**: Uses Groq's LLM (llama-3.1-70b-versatile) for natural language understanding and generation
- 🛍️ **Product Intelligence**: Retrieves and analyzes product data from DummyJSON API
- 💬 **Context-Aware Responses**: Understands user intent and provides relevant product information
- 🚀 **Fast & Scalable**: Built with FastAPI for high performance
- 📚 **Auto-Generated Documentation**: Interactive API docs with Swagger UI
- 🔍 **Smart Search**: Can handle various query types (product search, price inquiries, ratings, categories)

## Technology Stack

- **Backend Framework**: FastAPI
- **AI Model**: Groq LLM API (llama-3.1-70b-versatile)
- **Data Source**: DummyJSON Products API
- **HTTP Client**: HTTPX (async)
- **Validation**: Pydantic

## Project Structure

```
server/
├── app/
│   ├── api/
│   │   └── routes_chatbot.py      # API endpoint definitions
│   ├── core/
│   │   └── config.py              # Configuration and settings
│   ├── services/
│   │   ├── chatbot_service.py     # Chatbot logic and orchestration
│   │   └── product_service.py     # Product data fetching
│   ├── models/
│   │   └── schemas.py             # Pydantic models
│   ├── utils/
│   │   └── groq_client.py         # Groq API client
│   └── main.py                     # Application entry point
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
└── README.md                       # Documentation
```

## Installation

### Prerequisites

- Python 3.9+
- Groq API key (get it free at [console.groq.com](https://console.groq.com))

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd server
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your Groq API key:
   ```
   GROQ_API_KEY=your_actual_groq_api_key_here
   ```

5. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

   The API will be available at `http://localhost:8000`

## API Endpoints

### 1. GET `/api/products`

Fetch all products from DummyJSON API.

**Response:**
```json
{
  "products": [...],
  "total": 194,
  "skip": 0,
  "limit": 194
}
```

### 2. POST `/api/chat`

Send a message to the chatbot and receive an AI-generated response.

**Request:**
```json
{
  "message": "Tell me more about Kiwi"
}
```

**Response:**
```json
{
  "response": "Kiwi is a nutrient-rich fruit priced at $2.49, rated 4.9 stars by our customers. It ships overnight and comes with a 6-month warranty."
}
```

### Example Queries

The chatbot can handle various types of questions:

- **Product Information**: "Tell me about iPhone"
- **Price Inquiries**: "What's the price of mango?"
- **Category Search**: "Show me electronics"
- **Rating-Based**: "Products with ratings above 4"
- **Reviews**: "What are the reviews for Kiwi?"
- **Availability**: "Is the laptop in stock?"

## Architecture & Design

### RAG-Style Architecture

The chatbot implements a Retrieval-Augmented Generation (RAG) approach:

1. **Intent Analysis**: User message is analyzed by Groq LLM to extract intent and entities
2. **Data Retrieval**: Relevant product data is fetched from DummyJSON API based on extracted entities
3. **Response Generation**: Retrieved data is formatted and passed to Groq LLM to generate a natural, conversational response

### Service Layer Pattern

- **ProductService**: Handles all interactions with DummyJSON API
- **ChatbotService**: Orchestrates the chatbot logic (intent → retrieval → generation)
- **GroqClient**: Manages communication with Groq LLM API

### Key Features

- **Async Operations**: All I/O operations are asynchronous for better performance
- **Error Handling**: Comprehensive error handling with appropriate HTTP status codes
- **Type Safety**: Pydantic models for request/response validation
- **Modular Design**: Clear separation of concerns for maintainability
- **Singleton Pattern**: Services instantiated once and reused

## Testing the API

### Using Swagger UI

1. Navigate to `http://localhost:8000/docs`
2. Explore and test endpoints interactively
3. View request/response schemas

### Using cURL

**Get all products:**
```bash
curl -X GET "http://localhost:8000/api/products"
```

**Chat with the bot:**
```bash
curl -X POST "http://localhost:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me about Kiwi"}'
```

### Using Python

```python
import requests

# Chat endpoint
response = requests.post(
    "http://localhost:8000/api/chat",
    json={"message": "What's the price of iPhone?"}
)
print(response.json())
```

## Configuration

All configuration is managed through environment variables and `app/core/config.py`:

- `GROQ_API_KEY`: Your Groq API key (required)
- `GROQ_MODEL`: LLM model to use (default: llama-3.1-70b-versatile)
- `GROQ_TEMPERATURE`: Temperature for response generation (default: 0.7)
- `GROQ_MAX_TOKENS`: Maximum tokens in response (default: 1024)

## Error Handling

The API provides clear error messages:

- `400 Bad Request`: Invalid input (empty message, etc.)
- `500 Internal Server Error`: Server-side errors with descriptive messages

## Development

### Running in Development Mode

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```



## License

MIT License

## Contact

