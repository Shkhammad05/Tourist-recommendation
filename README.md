# 🌍 AI-Powered Tourist Recommendation System

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
