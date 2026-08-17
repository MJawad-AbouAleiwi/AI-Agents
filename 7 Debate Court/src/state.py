import operator
from typing import Annotated, Dict, List, Optional, TypedDict

class ArgumentRecord(TypedDict):
    round: int
    role: str  # Advocate or opponent
    argument: str
    evidence: List[str]
    sources: List[str]

class JudgeEvaluation(TypedDict):
    round: int
    advocate_scores: Dict[str, float]
    opponent_scores: Dict[str, float]
    advocate_weaknesses: List[str]
    opponent_weaknesses: List[str]
    winner: str  # Advocate, opponent, or undecided
    needs_more_evidence: bool
    evidence_requested_from: List[str]
    evidence_request_reason: str
    summary: str

class DebateState(TypedDict):
    claim: str
    max_rounds: int
    round: int
    injected_evidence: Optional[str]
    injected_evidence_side: Optional[str]  # Advocate, opponent, or both
    advocate_history: Annotated[List[ArgumentRecord], operator.add]
    opponent_history: Annotated[List[ArgumentRecord], operator.add]
    judge_history: Annotated[List[JudgeEvaluation], operator.add]
    continue_debate: bool
    final_verdict: Optional[Dict]