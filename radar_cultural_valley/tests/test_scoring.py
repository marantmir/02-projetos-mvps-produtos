from radar.demo_data import load_demo_sources
from radar.scoring import build_unified_candidates, score_candidates


def test_score_candidates_returns_ranked_rows():
    sources = load_demo_sources()
    candidates = build_unified_candidates(sources)
    scored = score_candidates(candidates)
    assert not scored.empty
    assert "score_oportunidade" in scored.columns
    assert scored["score_oportunidade"].iloc[0] >= scored["score_oportunidade"].iloc[-1]
