Here's the complete README.md content you can copy and paste:

---

# 📚 Novel Memory - Prompt Builder for Novel Writing

A lightweight, mobile-friendly web application for building augmented prompts with memory context for novel writing. Designed to work with Gemini (or any LLM) without API costs - simply copy and paste!

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
- Auto-detect matching memory entries by exact key match
- Manual selection from sidebar to add entries that weren't auto-detected
- Customizable instruction for the AI
- One-click copy of the augmented prompt

### 🔍 Extract Page
- Paste AI-generated story content
- Select entity types to extract (character, location, item, event, or custom)
- Generate extraction prompt for Gemini
- Extraction includes comprehensive narrative descriptions
- Multi-language support: Output matches input language

### 💾 Memory Management
- Import JSON from Gemini with smart merge
- Preview changes before applying
- Manual add/edit/delete entries
- Export all memory as JSON
- Data stored in browser localStorage

## 🏗️ Architecture

- **Frontend**: Stores all data in localStorage, handles UI
- **Backend**: Stateless calculations only (search, merge, prompt building)

## 📁 Project Structure

```
novel-prompt-builder/
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── search.py
│   │   ├── merge.py
│   │   └── prompt.py
│   └── static/
│       ├── index.html
│       ├── extract.html
│       ├── memory.html
│       └── css/
│           └── styles.css
├── requirements.txt
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- pip

### Installation

1. Clone the repository
```bash
git clone https://github.com/nvejkan/novel-prompt-builder.git
cd novel-prompt-builder
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the server
```bash
cd backend
python main.py
```

4. Open in browser
```
http://localhost:3010
```

## 📖 Usage Guide

### Step 1: Add Initial Memory

Go to Memory page and add entries manually or import JSON:

```json
{
  "Jon Snow": {
    "type": "character",
    "desc": "A brave knight of the Night's Watch with dark curly hair and grey eyes."
  },
  "Castle Black": {
    "type": "location",
    "desc": "The primary headquarters of the Night's Watch at the base of the Wall."
  }
}
```

### Step 2: Write with Context

1. Go to Prompt Builder page
2. Type or paste your story
3. Matching entries auto-detect
4. Click Copy Prompt
5. Paste into Gemini

### Step 3: Extract New Entities

1. Copy Gemini's response
2. Go to Extract page
3. Paste the story and click Copy Prompt
4. Paste into Gemini to get extracted entities as JSON

### Step 4: Update Memory

1. Go to Memory page
2. Paste the JSON from Gemini
3. Click Preview Merge then Apply Merge

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | Prompt Builder page |
| GET | /extract | Extraction page |
| GET | /memory | Memory Management page |
| POST | /api/search | Find matching keys in text |
| POST | /api/merge/preview | Preview merge operation |
| POST | /api/merge/apply | Apply merge |
| POST | /api/prompt/build | Build augmented prompt |
| POST | /api/prompt/extract | Build extraction prompt |
| GET | /health | Health check |

API docs available at: `http://localhost:3010/docs`

## 📱 Mobile Support

The UI is fully responsive and mobile-friendly.

## 🌐 Multi-Language Support

The extraction prompt automatically outputs in the same language as your story.

## 💾 Data Storage

All data is stored in your browser's localStorage. Export JSON for backup.

## 📄 License

This project is licensed under the MIT License.

---

Made with ❤️ for writers who love AI assistance but hate inconsistency.

---

Copy everything above and paste it into your `README.md` file. Let me know if you need any changes!