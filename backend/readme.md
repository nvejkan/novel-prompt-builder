# README.md

```markdown
# 📚 Novel Memory - Prompt Builder for Novel Writing

A lightweight, mobile-friendly web application for building augmented prompts with memory context for novel writing. Designed to work with Gemini (or any LLM) without API costs - simply copy and paste!

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-green.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-teal.svg)

## 🎯 Purpose

When writing novels with AI assistance, maintaining consistency across characters, locations, items, and events is challenging. This tool helps you:

1. **Store memory** of all entities in your story (characters, locations, items, events)
2. **Auto-detect** entities mentioned in your writing
3. **Build augmented prompts** that include relevant context
4. **Extract new entities** from AI-generated content back into memory

**No API costs!** - This app doesn't call any AI APIs. You copy the generated prompts to Gemini (or any LLM) manually.

## ✨ Features

### 📝 Prompt Builder (Main Page)
- Write or paste your story
- **Auto-detect** matching memory entries by exact key match
- **Manual selection** from sidebar to add entries that weren't auto-detected
- **Customizable instruction** for the AI
- **One-click copy** of the augmented prompt

### 🔍 Extract Page
- Paste AI-generated story content
- Select entity types to extract (character, location, item, event, or custom)
- Generate extraction prompt for Gemini
- Extraction includes **comprehensive narrative descriptions**:
  - **Characters**: appearance, traits, background, objectives, relationships
  - **Locations**: geography, appearance, purpose, owner, atmosphere
  - **Items**: description, special properties, origin, current status
  - **Events**: what, when, where, who, why, consequences
- **Multi-language support**: Output matches input language (English, Thai, Japanese, etc.)

### 💾 Memory Management
- Import JSON from Gemini with **smart merge**:
  - ✅ **New**: Entries that don't exist
  - ⚠️ **Update**: Entries that exist but have different content (with diff preview)
  - ⏭️ **Skip**: Entries that are identical
- **Checkbox control** for each merge item
- Manual add/edit/delete entries
- Export all memory as JSON
- Data stored in **browser localStorage** (persists across sessions)

## 🏗️ Architecture

```
┌─────────────────┐         ┌─────────────────┐
│                 │         │                 │
│  Browser        │  HTTP   │  Python Backend │
│  (Frontend)     │◄───────►│  (FastAPI)      │
│                 │         │                 │
│  - localStorage │         │  - Search       │
│  - UI/UX        │         │  - Merge logic  │
│  - Data storage │         │  - Prompt build │
│                 │         │                 │
└─────────────────┘         └─────────────────┘
     Storage                   Calculation
     (Stateful)                (Stateless)
```

- **Frontend**: Stores all data in localStorage, handles UI
- **Backend**: Stateless calculations only (search, merge, prompt building)

## 📁 Project Structure

```
novel-prompt-builder/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── models.py            # Pydantic models
│   ├── services/
│   │   ├── __init__.py
│   │   ├── search.py        # Keyword search logic
│   │   ├── merge.py         # Smart merge logic
│   │   └── prompt.py        # Prompt building
│   └── static/
│       ├── index.html       # Prompt Builder page
│       ├── extract.html     # Extraction page
│       ├── memory.html      # Memory Management page
│       └── css/
│           └── styles.css   # Mobile-friendly styles
├── requirements.txt
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/novel-prompt-builder.git
   cd novel-prompt-builder
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the server**
   ```bash
   cd backend
   python main.py
   ```

4. **Open in browser**
   ```
   http://localhost:3010
   ```

### Using Docker (Optional)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend/

EXPOSE 3010

CMD ["python", "backend/main.py"]
```

```bash
docker build -t novel-prompt-builder .
docker run -p 3010:3010 novel-prompt-builder
```

## 📖 Usage Guide

### Step 1: Add Initial Memory

Go to **Memory** page and either:

**Option A: Manual Entry**
1. Click "Add New Entry"
2. Enter Key (e.g., "Jon Snow"), Type (e.g., "character"), and Description
3. Click Save

**Option B: Import JSON**
```json
{
  "Jon Snow": {
    "type": "character",
    "desc": "A brave knight of the Night's Watch with dark curly hair and grey eyes. He is honorable and brooding, secretly a Targaryen prince. Wields the Valyrian steel sword Longclaw."
  },
  "Castle Black": {
    "type": "location",
    "desc": "The primary headquarters of the Night's Watch, located at the base of the Wall. A stark, ancient fortress built of dark stone, weathered by centuries of harsh winters."
  },
  "Longclaw": {
    "type": "item",
    "desc": "A Valyrian steel bastard sword with a white wolf-head pommel. Lighter and sharper than ordinary steel, capable of killing White Walkers. Gifted to Jon Snow by Lord Commander Mormont."
  }
}
```

### Step 2: Write with Context

1. Go to **Prompt Builder** page
2. Type or paste your story
3. Matching entries auto-detect (or click sidebar to add manually)
4. Optionally customize the instruction
5. Click **Copy Prompt**
6. Paste into Gemini and get AI-generated continuation

### Step 3: Extract New Entities

1. Copy Gemini's response
2. Go to **Extract** page
3. Paste the story
4. Adjust entity types if needed
5. Click **Copy Prompt**
6. Paste into Gemini to get extracted entities as JSON
7. Copy Gemini's JSON response

### Step 4: Update Memory

1. Go to **Memory** page
2. Paste the JSON from Gemini
3. Click **Preview Merge**
4. Review changes (check/uncheck items)
5. Click **Apply Merge**

### Repeat!

Continue the cycle: Write → Generate → Extract → Merge → Write...

## 🔌 API Endpoints

All endpoints are stateless - data is passed from frontend.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Prompt Builder page |
| `GET` | `/extract` | Extraction page |
| `GET` | `/memory` | Memory Management page |
| `POST` | `/api/search` | Find matching keys in text |
| `POST` | `/api/merge/preview` | Preview merge operation |
| `POST` | `/api/merge/apply` | Apply merge, return new memory |
| `POST` | `/api/prompt/build` | Build augmented prompt |
| `POST` | `/api/prompt/extract` | Build extraction prompt |
| `GET` | `/health` | Health check |

### API Documentation

Interactive API docs available at:
```
http://localhost:3010/docs
```

## 📱 Mobile Support

The UI is fully responsive and mobile-friendly:
- Collapsible sidebar on small screens
- Touch-friendly buttons and tags
- Responsive text areas
- Bottom action buttons for easy thumb access

## 🌐 Multi-Language Support

The extraction prompt automatically detects and outputs in the same language as your story:
- English → English output
- ไทย → Thai output
- 日本語 → Japanese output
- And more...

## 💾 Data Storage

All data is stored in your browser's **localStorage**:
- Data persists across browser sessions
- Data is private to your browser
- No server-side storage
- Export/import JSON for backup

**Key**: `novel_memory`

To manually backup:
```javascript
// In browser console
console.log(localStorage.getItem('novel_memory'));
```

## 🛠️ Configuration

### Change Port

Edit `backend/main.py`:
```python
uvicorn.run(
    "main:app",
    host="0.0.0.0",
    port=3010,  # Change this
    reload=True
)
```

### Customize Default Instruction

Edit `backend/services/prompt.py`:
```python
DEFAULT_INSTRUCTION = (
    "Your custom instruction here..."
)
```

### Add Default Entity Types

Edit `backend/services/prompt.py`:
```python
DEFAULT_EXTRACT_TYPES = ["character", "location", "item", "event", "organization"]
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Designed for use with [Google Gemini](https://gemini.google.com/)
- Inspired by the need for consistent novel writing with AI assistance

## 📞 Support

If you have any questions or issues, please open an issue on GitHub.

---

Made with ❤️ for writers who love AI assistance but hate inconsistency.
```
