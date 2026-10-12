from fastapi import APIRouter, HTTPException
import uuid
from app.schemas.scan import ScanRequest, ScanResponse, VerdictState
from app.core.scoring import calculate_mock_score
from app.core.explainer import generate_explanation

router = APIRouter(prefix="/api/v1/scan", tags=["Scanning"])

@router.post("/qr", response_model=ScanResponse)
async def scan_qr(request: ScanRequest):
    if not request.vpa:
        raise HTTPException(status_code=400, detail="VPA is required in the QR data.")
    
    # 1. Run scoring engine
    score_result = calculate_mock_score(request)
    
    # 2. Generate explanation using LLM based on signals and language
    explanation = generate_explanation(
        verdict=score_result["verdict"],
        signals=score_result["signals"],
        language=request.language
    )
    
    # 3. Assemble response
    return ScanResponse(
        request_id=str(uuid.uuid4())[:8],
        verdict=score_result["verdict"],
        safety_score=score_result["safety_score"],
        explanation=explanation,
        signals=score_result["signals"],
        graph_context=score_result["graph_context"],
        recommended_actions=["Do not authorize this payment if unfamiliar"] if score_result["verdict"] == VerdictState.red else [],
        can_report=True
    )

@router.post("/vpa", response_model=ScanResponse)
async def scan_vpa(request: ScanRequest):
    # For now, it delegates to the same logic
    return await scan_qr(request)
