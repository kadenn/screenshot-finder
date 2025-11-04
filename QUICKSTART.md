# Quick Start Guide

## Initial Setup

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your OpenAI API key
echo "OPENAI_API_KEY=sk-your-api-key-here" > .env
```

### 2. Add Screenshots

```bash
# Add your screenshot images to the screenshots folder
cp /path/to/your/screenshots/* ../screenshots/
```

### 3. Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install
```

## Running the App

### Terminal 1 - Backend

```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
uvicorn main:app --reload
```

✅ Backend running at http://localhost:8000

### Terminal 2 - Frontend

```bash
cd frontend
npm run dev
```

✅ Frontend running at http://localhost:5173

## Usage

1. Open http://localhost:5173 in your browser
2. Type natural language queries like:
   - "show me code screenshots"
   - "find graphs or charts"
   - "screenshots with emails"
   - "images showing terminals"

## Adding More Screenshots

1. Add new images to `/screenshots` folder
2. Restart backend (it will auto-index new files)
   - OR call `POST http://localhost:8000/api/reindex`

## Troubleshooting

**No screenshots found?**
- Check that images are in `/screenshots` folder
- Supported formats: jpg, jpeg, png, gif, webp

**OpenAI API Error?**
- Verify `OPENAI_API_KEY` in `backend/.env`
- Ensure you have GPT-4 or GPT-5 access

**CORS Error?**
- Make sure backend is on port 8000
- Make sure frontend is on port 5173

