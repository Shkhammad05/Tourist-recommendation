import time
from src.services.ranking import POIRankingService
from src.services.reasoning import LLMReasoningService
from src.services.retrieval import TouristRetrievalService


def print_banner():
    print("=" * 75)
    print("       AI-POWERED TOURIST RECOMMENDATION SYSTEM (HYBRID PIPELINE)       ")
    print("=" * 75)
    print(" Architecture: Dense Vector Retrieval -> Multi-Factor Ranking -> LLM")
    print("-" * 75)


def run_demo():
    print_banner()

    # 1. Warm-up and load models into memory
    print("\n[Init] Initializing Vector Embeddings, Qdrant & Ranking Services...")
    t_start = time.perf_counter()
    retrieval_svc = TouristRetrievalService()
    ranking_svc = POIRankingService()
    reasoning_svc = LLMReasoningService()
    init_time = (time.perf_counter() - t_start) * 1000
    print(f"[Init] Ready! Services loaded in {init_time:.2f} ms.\n")

    # 2. Interactive user inputs
    print("Enter Travel Preferences (Press Enter to use defaults):")
    city = input("  City [default: Paris]: ").strip() or "Paris"
    query = (
        input("  What are you looking for? [default: quiet peaceful art and paintings]: ").strip()
        or "quiet peaceful art and paintings"
    )
    budget_raw = input("  Max Budget (1: $, 2: $$, 3: $$$, 4: $$$$) [default: 2]: ").strip() or "2"
    top_k_raw = input("  How many spots to recommend? [default: 2]: ").strip() or "2"

    max_budget = int(budget_raw)
    top_k = int(top_k_raw)

    # Reference coordinates for Paris center (City Center demo)
    user_lat, user_lon = 48.8566, 2.3522

    print("\n" + "-" * 75)
    print(f"Executing End-to-End Inference for: '{query}' in {city} (Budget <= {max_budget})...")
    print("-" * 75)

    pipeline_start = time.perf_counter()

    # Stage 1: Dense Vector Retrieval + Hard Metadata Filters
    t0 = time.perf_counter()
    candidates = retrieval_svc.search(
        query=query,
        city=city,
        max_budget_level=max_budget,
        top_k=max(top_k * 2, 4),
    )
    t_retrieval = (time.perf_counter() - t0) * 1000

    if not candidates:
        print(f"\n[Result] No POIs matched your filters for '{city}' with budget level {max_budget}.")
        return

    # Stage 2: Heavy Scoring & Multi-Factor Re-ranking
    t1 = time.perf_counter()
    ranked_candidates = ranking_svc.rank(
        candidates=candidates,
        user_lat=user_lat,
        user_lon=user_lon,
    )
    top_matches = ranked_candidates[:top_k]
    t_ranking = (time.perf_counter() - t1) * 1000

    # Stage 3: LLM Contextual Reasoning
    t2 = time.perf_counter()
    final_recommendations = reasoning_svc.generate_justifications(
        query=query,
        pois=top_matches,
    )
    t_reasoning = (time.perf_counter() - t2) * 1000

    total_pipeline_time = (time.perf_counter() - pipeline_start) * 1000

    # 3. Formatted Output Presentation
    print("\n" + "=" * 75)
    print("                     TOP RECOMMENDATIONS                     ")
    print("=" * 75)

    for idx, poi in enumerate(final_recommendations, 1):
        budget_str = "$" * poi.get("budget_level", 1)
        dist_str = f"{poi.get('distance_km')} km" if poi.get("distance_km") is not None else "N/A"
        print(f"\n[{idx}] {poi['name'].upper()} ({poi['category']})")
        print(f"    Rating: {poi['rating']}/5.0  |  Budget: {budget_str}  |  Distance: {dist_str}")
        print(f"    Similarity Match: {poi['similarity_score'] * 100:.1f}%  |  Final Composite Score: {poi['ranking_score']}")
        print(f"    Overview: {poi['description']}")
        print(f"    AI Rationale: {poi['justification']}")

    # 4. Latency breakdown for external viva
    print("\n" + "=" * 75)
    print("                      LATENCY METRICS BREAKDOWN                      ")
    print("=" * 75)
    print(f"  • Stage 1 (Vector Search + Filter) : {t_retrieval:.2f} ms")
    print(f"  • Stage 2 (Multi-factor Re-ranking): {t_ranking:.2f} ms")
    print(f"  • Stage 3 (Reasoning Layer)        : {t_reasoning:.2f} ms")
    print(f"  • Total End-to-End Latency         : {total_pipeline_time:.2f} ms")
    print("=" * 75)


if __name__ == "__main__":
    run_demo()