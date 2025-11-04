# Screenshot Search App

A monorepo screenshot search application that uses GPT-5 vision API to analyze and index screenshots, with a simple chat interface for natural language queries.

<img width="1296" height="884" alt="image" src="https://github.com/user-attachments/assets/4d2eaa73-0c43-4f6b-9467-168bf03f0c61" />


## Features

- **Auto-indexing**: Backend automatically scans and indexes all screenshots from `/screenshots` folder on startup
- **GPT-5 Vision**: Uses OpenAI's GPT-5 (gpt-4o) to analyze images and extract metadata
- **Natural Language Search**: Chat interface powered by GPT-5 agent for intelligent screenshot search
- **Confidence Scores**: Each result shows relevance confidence (0-100%)
- **Full-size Preview**: Click thumbnails to view full-size images

## Project Structure

```
screenshot-finder/
├── backend/          # Python FastAPI API
├── frontend/         # Vue 3 + Tailwind UI
├── screenshots/      # Your screenshots (add images here)
└── README.md
```

## Setup

### Prerequisites

- Python 3.9+
- Node.js 18+
- OpenAI API key with GPT-4 or GPT-5 access

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```bash
echo "OPENAI_API_KEY=your-api-key-here" > .env
```

5. Add screenshots to the `/screenshots` folder:
```bash
# Copy your screenshot images to ../screenshots/
```

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

## Running the Application

### Start Backend (Terminal 1)

```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn main:app --reload
```

Backend will start on `http://localhost:8000`

The backend will automatically:
- Initialize the SQLite database
- Scan `/screenshots` folder
- Index new screenshots using GPT-5 vision API

### Start Frontend (Terminal 2)

```bash
cd frontend
npm run dev
```

Frontend will start on `http://localhost:5173`

## Usage

1. **Add Screenshots**: Place your screenshot images in the `/screenshots` folder
2. **Start Backend**: The backend will automatically index them on startup
3. **Open UI**: Navigate to `http://localhost:5173`
4. **Search**: Type natural language queries like:
   - "show me code screenshots"
   - "find graphs or charts"
   - "screenshots with emails"
   - "images with terminal or command line"

## API Endpoints

- `POST /api/chat` - Search screenshots with natural language query
- `GET /api/images/{filename}` - Serve screenshot image files
- `POST /api/reindex` - Manually trigger re-indexing
- `GET /api/stats` - Get indexing statistics

## Tech Stack

### Backend
- FastAPI - Web framework
- OpenAI GPT-5 - Image analysis and search
- SQLite - Screenshot metadata storage
- Pillow - Image processing

### Frontend
- Vue 3 (Composition API)
- Vite - Build tool
- Tailwind CSS - Styling
- Axios - HTTP client

## Configuration

### Supported Image Formats
- JPG/JPEG
- PNG
- GIF
- WebP

### Environment Variables

Create a `.env` file in the `backend` directory:

```env
OPENAI_API_KEY=sk-your-api-key-here
```

## Development

### Backend Development

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development

```bash
cd frontend
npm run dev
```

### Building Frontend for Production

```bash
cd frontend
npm run build
```

## Troubleshooting

### No screenshots found
- Ensure screenshots are in the `/screenshots` folder at the root of the project
- Supported formats: jpg, jpeg, png, gif, webp

### API Key Error
- Verify your OpenAI API key is set in `backend/.env`
- Ensure you have access to GPT-4 or GPT-5 models

### CORS Error
- Backend and frontend must run on localhost:8000 and localhost:5173 respectively
- Check CORS configuration in `backend/main.py`

### Re-indexing
- Add new screenshots to `/screenshots` folder
- Restart backend OR call `POST http://localhost:8000/api/reindex`

## License

MIT

