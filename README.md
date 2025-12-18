# 🛒 BuyBuddy - Intelligent Shopping Agent

An intelligent product search service that allows users to specify what they want to buy and finds corresponding products on the internet.

BuyBuddy leverages AI agents to understand user queries, research products, compare prices, and provide intelligent shopping recommendations.

## ✨ Features

- 🤖 **AI-Powered Query Understanding**: Natural language processing to understand user shopping intent
- 🔍 **Intelligent Product Research**: Multi-source product search with price comparison
- 💬 **Conversational Interface**: Chat-based interaction for seamless shopping assistance
- 🔄 **Multi-LLM Support**: Flexible LLM provider system (Ollama, DeepSeek, OpenAI)
- 🎯 **Workflow-Based Architecture**: LangGraph-powered state management for complex shopping workflows

## 🚀 Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: React + Vite + TailwindCSS
- **API de recherche**: SerperDev (products with prices)
- **LLM**: Multi-provider support (Ollama, DeepSeek, OpenAI) - easily swappable
- **Agents**: Query Understanding + Product Researcher + Price Comparator + Conversation Handler
- **Workflow Engine**: LangGraph for state management

## 📋 Project Status

- ✅ Backend FastAPI functional
- ✅ SerperDev API configured and tested
- ✅ Query Understanding Agent (understands user queries)
- ✅ Product Researcher Agent (intelligent product search)
- ✅ Price Comparator Agent
- ✅ Conversation Handler Agent
- ✅ Frontend React interface
- ✅ LangGraph workflow implementation

## 🏃 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 18+
- An API key from [SerperDev](https://serper.dev/)
- (Optional) An LLM provider API key (Ollama, DeepSeek, or OpenAI)

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the `backend` directory:
```env
# Search API (Required)
SERPER_API_KEY=your_serper_api_key

# LLM Provider (choose one)
LLM_PROVIDER=ollama  # Options: ollama, deepseek, openai

# Ollama (if LLM_PROVIDER=ollama)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=qwen2.5:7b

# DeepSeek (if LLM_PROVIDER=deepseek)
DEEPSEEK_API_KEY=your_deepseek_api_key

# OpenAI (if LLM_PROVIDER=openai)
OPENAI_API_KEY=your_openai_api_key
```

5. Start the backend server:
```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## 📚 API Documentation

Once the backend is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Main Endpoints

- `POST /api/v1/chat` - Chat with the shopping agent
- `POST /api/v1/search` - Direct product search
- `GET /api/v1/health` - Health check

## 🧪 Testing

### Test Product Search
```powershell
# Windows PowerShell
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/search" -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"query":"laptop gaming"}'
```

```bash
# macOS/Linux
curl -X POST "http://localhost:8000/api/v1/search" \
  -H "Content-Type: application/json" \
  -d '{"query":"laptop gaming"}'
```

### Test Chat Interface
```powershell
# Windows PowerShell
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/chat" -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"message":"I want a gaming laptop under $1500"}'
```

## 🏗️ Architecture

The project follows a clean architecture pattern:

```
backend/
├── app/
│   ├── agents/          # AI agents (query understanding, product research, etc.)
│   ├── api/             # FastAPI routes
│   ├── core/            # Configuration and database
│   ├── infrastructure/  # External APIs and LLM providers
│   ├── models/          # Data models and schemas
│   └── workflows/       # LangGraph workflows
└── main.py              # Application entry point

frontend/
├── src/
│   ├── components/      # React components
│   ├── hooks/           # Custom React hooks
│   └── App.jsx          # Main application component
```

## 🔧 Configuration

**Switching LLM Providers**: Simply change the `LLM_PROVIDER` value in your `.env` file. No code changes required!

Supported providers:
- **Ollama**: Local LLM deployment (free, requires local setup)
- **DeepSeek**: Cloud-based LLM (cost-effective)
- **OpenAI**: GPT models (premium quality)

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For questions or support, please open an issue on GitHub.

