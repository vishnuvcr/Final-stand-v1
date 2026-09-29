from holdout import CANDIDATE_STOPS, SELECTION_SLIPPAGE

def test_candidate_protocol():
    assert CANDIDATE_STOPS == [25.0, 50.0, 75.0, 100.0, 150.0, 200.0, 300.0]
    assert SELECTION_SLIPPAGE == 0.50

if __name__ == "__main__":
    test_candidate_protocol()
    print("Phase 13W tests passed.")
