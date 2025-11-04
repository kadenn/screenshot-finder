# Backend - Screenshot Search API

FastAPI backend that uses GPT-5 vision API to analyze and index screenshots.

## Quick Start

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file:
```bash
echo "OPENAI_API_KEY=your-api-key-here" > .env
```

4. Add screenshots to `../screenshots/` folder

5. Run the server:
```bash
uvicorn main:app --reload
```

The server will start on http://localhost:8000 and automatically index screenshots on startup.

## API Endpoints

- `GET /` - API info
- `POST /api/chat` - Search screenshots
- `GET /api/images/{filename}` - Serve images
- `POST /api/reindex` - Re-index screenshots
- `GET /api/stats` - Get statistics

## Database

SQLite database (`screenshots.db`) stores:
- filename
- filepath
- metadata (GPT-5 generated JSON)
- indexed_at timestamp

