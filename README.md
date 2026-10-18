🌍 AI-Powered Tourist Recommendation SystemAn intelligent, multi-stage tourist recommendation engine built using FastAPI, Qdrant (Local Vector Search), Sentence-Transformers, and Pydantic.Unlike simple keyword-based search engines (like SQL LIKE queries), this system understands semantic travel intent (e.g., "calm sunset walk near sea" matching with "Marine Drive" or "Palolem Beach") and scores places dynamically using physical distance and ratings.📌 Key HighlightsDense Semantic Retrieval: Converts natural language user queries into 384-dimensional dense vectors using BAAI/bge-small-en-v1.5.Hybrid Multi-Factor Scoring: Re-ranks candidates by combining semantic cosine similarity, user ratings, and Haversine geographical distance decay.No Heavy Infrastructure Required: Runs locally without Docker using Qdrant's embedded disk storage mode.Explainable Output: Generates context-aware rationale for why each spot was recommended.Sub-50ms Latency: Ultra-fast execution suitable for real-time mobile and web applications.🏛️ System ArchitectureThe recommendation pipeline operates as a 3-stage funnel:                  User Query + City + Coordinates
                                │
                                ▼
  ┌──────────────────────────────────────────────────────────┐
  │  Stage 1: Candidate Retrieval (Qdrant + Dense Embeddings) │
  │  • Encodes query into 384-d vector                       │
  │  • Applies hard filters: City & Budget Level             │
  │  • Retrieves candidate pool via Cosine Similarity        │
  └─────────────────────────────┬────────────────────────────┘
                                │
                                ▼
  ┌──────────────────────────────────────────────────────────┐
  │  Stage 2: Multi-Factor Re-ranking & Scoring              │
  │  • Calculates Great-Circle distance (Haversine formula)  │
  │  • Formula:                                              │
  │    Score = 0.50*(Similarity) + 0.30*(Rating/5)           │
  │            + 0.20*(Distance_Decay)                       │
  │  • Sorts and selects Top-K places                        │
  └─────────────────────────────┬────────────────────────────┘
                                │
                                ▼
  ┌──────────────────────────────────────────────────────────┐
  │  Stage 3: Context-Aware Reasoning Layer                  │
  │  • Enriches POIs with human-readable rationale           │
  │  • Features offline fallback for zero API downtime       │
  └─────────────────────────────┬────────────────────────────┘
                                │
                                ▼
              FastAPI JSON Response / Terminal UI
🛠️ Tech StackComponentTechnologyRoleBackend APIFastAPI + UvicornHigh-performance asynchronous REST APIData ValidationPydantic v2Strict request/response schema contractsVector DatabaseQdrant (Local Embedded)In-memory / disk-backed vector indexingEmbedding ModelBAAI/bge-small-en-v1.5Semantic text encoding (HuggingFace)Spatial MathHaversine Formula (Custom)Great-circle spherical distance computation📂 Project Directory Structuretourist-recommender/
├── src/
│   ├── api/
│   │   ├── main.py            # FastAPI server & route handlers
│   │   └── schemas.py         # Request and Response Pydantic models
│   ├── pipeline/
│   │   └── ingest.py          # Vectorization and Qdrant indexing script
│   └── services/
│       ├── ranking.py         # Multi-factor re-ranking & Haversine distance
│       ├── reasoning.py       # Justification generation service
│       └── retrieval.py       # Dense vector search with Qdrant filters
├── demo.py                    # Interactive CLI presentation demo script
├── requirements.txt           # Python package dependencies
├── .gitignore                 # Git ignore file for venv & cache
└── README.md                  # Project documentation
🚀 Setup & Execution Guide1. PrerequisitesPython 3.11 or 3.12 installedGit installed2. Clone Repository & Setup Virtual Environmentgit clone <your-repo-url>
cd tourist-recommender

# Create virtual environment
py -3.11 -m venv venv

# Activate virtual environment (Windows PowerShell)
.\venv\Scripts\Activate.ps1
3. Install Dependenciespip install -r requirements.txt
4. Index Dataset into QdrantIndex points of interest across Mumbai, Goa, and Paris:python src/pipeline/ingest.py
5. Run Live Terminal Demo (Viva / Presentation)python demo.py
6. Run FastAPI Serverpython -m uvicorn src.api.main:app --reload --port 8000
Open your browser to test endpoints interactively via Swagger UI:
👉 http://localhost:8000/docs📡 API ReferenceRecommend PlacesEndpoint: POST /api/v1/recommendHeaders: Content-Type: application/jsonSample Request Body:{
  "user_id": "usr_101",
  "query": "peaceful sunset beach and cool breeze",
  "city": "Mumbai",
  "latitude": 18.9432,
  "longitude": 72.8230,
  "max_budget_level": 2,
  "top_k": 2
}
Sample Response Body:{
  "user_id": "usr_101",
  "city": "Mumbai",
  "total_found": 2,
  "recommendations": [
    {
      "poi_id": 1,
      "name": "Marine Drive",
      "category": "Promenade / Seafront",
      "budget_level": 1,
      "rating": 4.8,
      "distance_km": 0.0,
      "similarity_score": 0.7241,
      "ranking_score": 0.8501,
      "description": "Scenic curved seafront boulevard overlooking the Arabian Sea, perfect for peaceful evening walks, sunsets, and sea breeze.",
      "justification": "Selected because it directly satisfies your interest in promenade / seafronts with a top community rating of 4.8/5.0."
    }
  ]
}
👨‍🏫 Viva Examination FAQWhy use Bi-Encoder embeddings over traditional SQL keyword matching?Keyword search requires exact words (e.g., searching "ocean" will miss "Arabian sea"). Bi-encoders convert text to semantic vector space where synonyms and contextual concepts map closely together.Why a 3-Stage pipeline instead of directly using an LLM?Sending thousands of places to an LLM is too slow and expensive. Stage 1 narrows down thousands of places to top candidates in milliseconds, Stage 2 re-ranks using business logic and physical distance, and Stage 3 uses AI only for explanation.Why Haversine formula instead of Euclidean distance?Earth is an oblate spheroid, not a flat plane. Euclidean distance produces significant distortion across long coordinate spans, whereas Haversine computes true great-circle distance on a sphere.
