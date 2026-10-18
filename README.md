Screenshot dekh kar lag raha hai ki saare points ek saath chipak gaye hain. Markdown formatting me headings, line breaks aur code blocks sahi se # 🌍 AI-Powered Tourist Recommendation System

A production-grade, local-first hybrid recommendation engine built with **FastAPI**, **Qdrant**, and **Sentence-Transformers**.

---

## 🚀 Key Features

* **3-Stage Hybrid Funnel:** Vector search, multi-factor heuristic ranking, and context-aware reasoning.
* **No Docker Needed:** Runs locally on disk using Qdrant embedded mode.
* **Low Latency:** Sub-50ms end-to-end inference time.
* **Explainable Output:** Generates clear justifications for every recommended spot.

---

## 🏛️ System Architecture

```text
User Query + City + Lat/Lon
       │
       ▼
[Stage 1: Candidate Retrieval]
 ├── Model: BAAI/bge-small-en-v1.5 (384-d)
 ├── Vector DB: Qdrant (Cosine Similarity)
 └── Hard Filtering: City & Budget Level
       │
       ▼
[Stage 2: Multi-Factor Re-ranking]
 ├── Haversine Distance Decay (User Lat/Lon)
 ├── Community Rating Normalization
 └── Composite Scoring Function
       │
       ▼
[Stage 3: LLM Contextual Reasoning]
 └── Generates 1-sentence personalized rationale

🛠️ Tech Stack
 * Framework: FastAPI, Uvicorn, Pydantic v2
 * Vector DB: Qdrant (Local Disk Storage)
 * Embeddings: HuggingFace BAAI/bge-small-en-v1.5
 * Language: Python 3.11
⚡ Quick Start
1. Setup Virtual Environment
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

2. Ingest Sample POI Data
python src/pipeline/ingest.py

3. Run FastAPI Backend
python -m uvicorn src.api.main:app --reload --port 8000

Swagger UI check karne ke liye: http://localhost:8000/docs
4. Run Interactive Demo
python demo.py

📬 Sample API Request
{
  "user_id": "usr_101",
  "query": "peaceful historic art museum",
  "city": "Paris",
  "latitude": 48.8566,
  "longitude": 2.3266,
  "max_budget_level": 2,
  "top_k": 2
}


