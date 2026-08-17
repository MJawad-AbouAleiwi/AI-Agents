from typing import Optional
from config import (
    HISTORY_WINDOW,
    NUM_PREDICT_ARGUMENT,
    NUM_PREDICT_FINAL,
    NUM_PREDICT_JUDGE,
    TEMPERATURE_DEBATER,
    TEMPERATURE_JUDGE,
)
from llm import call_json
from prompts import ADVOCATE_SYSTEM, FINAL_VERDICT_SYSTEM, JUDGE_SYSTEM, OPPONENT_SYSTEM
from state import DebateState

def _last_judge_feedback(state: DebateState) -> Optional[dict]:
    if not state["judge_history"]:
        return None
    return state["judge_history"][-1]

def _build_debater_prompt(state: DebateState, role: str) -> str:
    opponent_role = "opponent" if role == "advocate" else "advocate"
    own_history = state["advocate_history"] if role == "advocate" else state["opponent_history"]
    opp_history = state["opponent_history"] if role == "advocate" else state["advocate_history"]

    parts = [
        f"CLAIM: {state['claim']}",
        f"This is round {state['round'] + 1} of a maximum of {state['max_rounds']}.",
    ]

    if own_history:
        for rec in own_history[-HISTORY_WINDOW:]:
            parts.append(f"\nYour previous argument (round {rec['round'] + 1}):\n{rec['argument']}")

    if opp_history:
        for rec in opp_history[-HISTORY_WINDOW:]:
            parts.append(
                f"\n{opponent_role.upper()}'s argument you must rebut "
                f"(round {rec['round'] + 1}):\n{rec['argument']}"
            )
            if rec.get("evidence"):
                parts.append("Their evidence: " + "; ".join(rec["evidence"]))

    feedback = _last_judge_feedback(state)
    if feedback:
        weaknesses = feedback.get(f"{role}_weaknesses", [])
        if weaknesses:
            parts.append(
                "\nThe judge identified these weaknesses in your last argument -- "
                "fix them, don't just repeat yourself:\n- " + "\n- ".join(weaknesses)
            )
        if role in feedback.get("evidence_requested_from", []):
            parts.append(
                "\nThe judge specifically requested stronger evidence from you. "
                f"Reason: {feedback.get('evidence_request_reason', '')}"
            )

    if state.get("injected_evidence") and state.get("injected_evidence_side") in (role, "both"):
        parts.append(
            "\nNEW EVIDENCE has just been entered into the record. You must "
            f"account for it in your argument:\n{state['injected_evidence']}"
        )

    parts.append("\nRespond with ONLY the JSON object described in your system instructions.")
    return "\n".join(parts)

def advocate_node(state: DebateState) -> dict:
    user_prompt = _build_debater_prompt(state, "advocate")
    data = call_json(
        ADVOCATE_SYSTEM,
        user_prompt,
        temperature=TEMPERATURE_DEBATER,
        num_predict=NUM_PREDICT_ARGUMENT,
    )
    record = {
        "round": state["round"],
        "role": "advocate",
        "argument": data.get("argument", ""),
        "evidence": data.get("evidence", []),
        "sources": data.get("sources", []),
    }
    return {"advocate_history": [record]}

def opponent_node(state: DebateState) -> dict:
    user_prompt = _build_debater_prompt(state, "opponent")
    data = call_json(
        OPPONENT_SYSTEM,
        user_prompt,
        temperature=TEMPERATURE_DEBATER,
        num_predict=NUM_PREDICT_ARGUMENT,
    )
    record = {
        "round": state["round"],
        "role": "opponent",
        "argument": data.get("argument", ""),
        "evidence": data.get("evidence", []),
        "sources": data.get("sources", []),
    }
    return {"opponent_history": [record]}

def judge_node(state: DebateState) -> dict:
    adv = state["advocate_history"][-1]
    opp = state["opponent_history"][-1]

    user_prompt = f"""CLAIM: {state['claim']}

ADVOCATE argument (round {adv['round'] + 1}):
{adv['argument']}
Evidence: {adv['evidence']}
Source types: {adv['sources']}

OPPONENT argument (round {opp['round'] + 1}):
{opp['argument']}
Evidence: {opp['evidence']}
Source types: {opp['sources']}

This is round {state['round'] + 1} of a maximum of {state['max_rounds']}.
Evaluate strictly per the five criteria in your instructions."""

    data = call_json(
        JUDGE_SYSTEM,
        user_prompt,
        temperature=TEMPERATURE_JUDGE,
        num_predict=NUM_PREDICT_JUDGE,
    )

    evaluation = {
        "round": state["round"],
        "advocate_scores": data.get("advocate_scores", {}),
        "opponent_scores": data.get("opponent_scores", {}),
        "advocate_weaknesses": data.get("advocate_weaknesses", []),
        "opponent_weaknesses": data.get("opponent_weaknesses", []),
        "winner": data.get("winner", "undecided"),
        "needs_more_evidence": bool(data.get("needs_more_evidence", False)),
        "evidence_requested_from": data.get("evidence_requested_from", []),
        "evidence_request_reason": data.get("evidence_request_reason", ""),
        "summary": data.get("summary", ""),
    }

    next_round = state["round"] + 1
    continue_debate = evaluation["needs_more_evidence"] and next_round < state["max_rounds"]

    return {
        "judge_history": [evaluation],
        "round": next_round,
        "continue_debate": continue_debate,
    }

def final_verdict_node(state: DebateState) -> dict:
    rounds_summary = []
    for j in state["judge_history"]:
        rounds_summary.append(
            f"Round {j['round'] + 1}: winner={j['winner']}, "
            f"advocate_scores={j['advocate_scores']}, opponent_scores={j['opponent_scores']}, "
            f"advocate_weaknesses={j['advocate_weaknesses']}, "
            f"opponent_weaknesses={j['opponent_weaknesses']}, summary={j['summary']}"
        )
    last_adv = state["advocate_history"][-1]["argument"] if state["advocate_history"] else ""
    last_opp = state["opponent_history"][-1]["argument"] if state["opponent_history"] else ""
    user_prompt = f"""CLAIM: {state['claim']}

Full per-round judge record:
{chr(10).join(rounds_summary)}

Final advocate argument: {last_adv}
Final opponent argument: {last_opp}

Deliver your final, binding verdict based on the full record above."""

    data = call_json(
        FINAL_VERDICT_SYSTEM,
        user_prompt,
        temperature=TEMPERATURE_JUDGE,
        num_predict=NUM_PREDICT_FINAL,
    )

    return {"final_verdict": data}