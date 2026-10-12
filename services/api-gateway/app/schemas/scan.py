from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class VerdictState(str, Enum):
    green = "green"
    yellow = "yellow"
    red = "red"
    unable_to_verify = "unable_to_verify"

class Signal(BaseModel):
    code: str
    severity: str
    detail: Optional[str] = None

class GraphContext(BaseModel):
    connected_flagged_vpas: int

class ScanRequest(BaseModel):
    vpa: Optional[str] = None
    image_data: Optional[str] = None
    txn_type: str = "pay"
    amount: Optional[float] = None
    language: str = "english" # Added language parameter

class ScanResponse(BaseModel):
    request_id: str
    verdict: VerdictState
    safety_score: Optional[int]
    explanation: str
    signals: List[Signal]
    graph_context: Optional[GraphContext]
    recommended_actions: List[str]
    can_report: bool
