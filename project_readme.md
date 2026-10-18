# AI-Powered Tourist Recommendation System

A production-grade, 3-stage hybrid tourist recommendation engine built with **FastAPI**, **Qdrant (Local Vector DB)**, **Sentence-Transformers**, and **Pydantic**. Designed for real-time semantic discovery, heuristic re-ranking, and context-aware justifications without relying on heavy external infrastructure or Docker.

---

## 🏛️ System Architecture

The recommendation pipeline follows a standard modern search-and-recommend funnel:

```
[ User Query + City Filter + Coordinates ]
                   │
                   ▼
  Stage 1: Candidate Retrieval (Qdrant + BGE-Small)
     • Converts free-text intent to 384-d dense vector
     • Applies hard payload filters (City, Budget tier)
     • Returns candidate pool via Cosine Similarity
                   │
                   ▼
  Stage 2: Multi-Factor Scoring & Re-ranking
     • Haversine Spherical Distance calculation
     • Composite formula: 
       Score = 0.50*(Sim) + 0.30*(Rating/5) + 0.20*(Distance_Decay)
     • Truncates to top-k recommendations
                   │
                   ▼
  Stage 3: Context-Aware Reasoning Layer
     • Synthesizes user-facing rationale
     • Built-in graceful degradation for offline execution
                   │
                   ▼
[ FastAPI JSON Response / Interactive Terminal UI ]
```

---

## 🛠️ Tech Stack

- **Framework**: FastAPI, Uvicorn
- **Data Validation**: Pydantic v2
- **Vector Database**: Qdrant (Disk-backed local storage mode)
- **Embedding Model**: `BAAI/bge-small-en-v1.5` (Sentence-Transformers)
- **Math/Algorithms**: Haversine Spherical Distance Formula

---

## 📂 Repository Structure

```
tourist-recommender/
├── src/
│   ├── api/
│   │   ├── main.py            # FastAPI endpoints & Lifespan event handlers
│   │   └── schemas.py         # Pydantic input/output schemas
│   ├── pipeline/
│   │   └── ingest.py          # Data ingestion & vector indexing pipeline
│   └── services/
│       ├── ranking.py         # Haversine distance & composite scoring
│       ├── reasoning.py       # LLM justification service with fallback
│       └── retrieval.py       # Dense vector search via Qdrant
├── demo.py                    # Interactive terminal testing script
├── requirements.txt           # Project dependencies
├── .gitignore
└── README.md
```

---

## 🚀 Quickstart Guide

### 1. Clone & Set Up Environment
```powershell
git clone <your-github-repo-url>
cd tourist-recommender

# Create and activate virtual environment (Python 3.11 recommended)
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 2. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 3. Initialize & Index Dataset
Index the multi-city dataset (Mumbai, Goa, Paris) into the local vector store:
```powershell
python src/pipeline/ingest.py
```

### 4. Run Interactive Demo (Viva / Presentation Mode)
```powershell
python demo.py
```

### 5. Launch FastAPI Backend
```powershell
uvicorn src.api.main:app --reload --port 8000
```
Access the interactive OpenAPI Swagger docs at:  
👉 **`http://localhost:8000/docs`**

---

## 📊 Sample API Request

**Endpoint**: `POST /api/v1/recommend`

```json
{
  "user_id": "usr_101",
  "query": "quiet sunset sea view",
  "city": "Mumbai",
  "latitude": 18.9220,
  "longitude": 72.8347,
  "max_budget_level": 2,
  "top_k": 2
}
```