from app.schemas.scan import ScanRequest, VerdictState, Signal, GraphContext

# Mock seeded VPA databases for Checkpoint 2
VERIFIED_MERCHANTS = ["trusted_merchant@upi", "amazon@upi"]
MOCK_REPORTS = {
    "scam1@upi": 1,
    "scam2@upi": 2,
    "scam3@upi": 4, # 3+ reports
    "newguy@upi": 0
}

def calculate_mock_score(request: ScanRequest):
    if request.vpa == "invalid@upi":
        # Simulate unable to verify
        return {
            "verdict": VerdictState.unable_to_verify,
            "safety_score": None,
            "signals": [Signal(code="INVALID_VPA", severity="n/a")],
            "graph_context": None
        }

    score = 50
    signals = []
    
    # 1. Verified Merchant
    if request.vpa in VERIFIED_MERCHANTS:
        score += 40
        signals.append(Signal(code="VERIFIED_MERCHANT", severity="low", detail="Known trusted merchant"))

    # 2. Community Reports
    reports = MOCK_REPORTS.get(request.vpa, 0)
    if reports == 1:
        score -= 10
        signals.append(Signal(code="VPA_SINGLE_REPORT", severity="medium", detail="1 report in the last 7 days"))
    elif reports == 2:
        score -= 25
        signals.append(Signal(code="VPA_MULTIPLE_REPORTS", severity="high", detail="2 reports in the last 7 days"))
    elif reports >= 3:
        score -= 40
        signals.append(Signal(code="VPA_MANY_REPORTS", severity="critical", detail=f"{reports} reports in the last 7 days"))
        
    # 3. Transaction Type (Collect)
    if request.txn_type == "collect":
        score -= 25
        signals.append(Signal(code="COLLECT_DISGUISED_AS_PAY", severity="high", detail="Request to receive money, not pay"))
        
    # Hard cap for 3+ reports
    if reports >= 3:
        score = min(score, 20)
        
    # Cap score between 0 and 100
    score = max(0, min(100, score))
    
    # Verdict bands
    if score >= 70:
        verdict = VerdictState.green
    elif score >= 40:
        verdict = VerdictState.yellow
    else:
        verdict = VerdictState.red

    return {
        "verdict": verdict,
        "safety_score": score,
        "signals": signals,
        "graph_context": GraphContext(connected_flagged_vpas=reports) if reports > 0 else None
    }
