import argparse
import json
from config import MAX_ROUNDS_DEFAULT
from graph import build_graph
try:
    from rich.console import Console
    from rich.panel import Panel
    RICH = True
    console = Console()
except ImportError:  # Keep the tool usable
    RICH = False

def _print(title: str, body: str, style: str = "white") -> None:
    if RICH:
        console.print(Panel(body, title=title, border_style=style))
    else:
        print(f"\n=== {title} ===\n{body}\n")

def run_debate(
    claim: str,
    max_rounds: int = MAX_ROUNDS_DEFAULT,
    injected_evidence: str = None,
    injected_evidence_side: str = None,
) -> dict:
    app = build_graph()
    initial_state = {
        "claim": claim,
        "max_rounds": max_rounds,
        "round": 0,
        "injected_evidence": injected_evidence,
        "injected_evidence_side": injected_evidence_side,
        "advocate_history": [],
        "opponent_history": [],
        "judge_history": [],
        "continue_debate": False,
        "final_verdict": None,
    }
    # Recursion_limit guards against runaway loops
    return app.invoke(initial_state, config={"recursion_limit": 50})

def print_transcript(state: dict) -> None:
    _print("CLAIM", state["claim"], style="bold cyan")

    n_rounds = max(len(state["advocate_history"]), len(state["opponent_history"]))
    for i in range(n_rounds):
        if i < len(state["advocate_history"]):
            a = state["advocate_history"][i]
            body = a["argument"]
            if a["evidence"]:
                body += "\n\nEvidence:\n- " + "\n- ".join(a["evidence"])
            _print(f"ADVOCATE -- Round {i + 1}", body, style="green")

        if i < len(state["opponent_history"]):
            o = state["opponent_history"][i]
            body = o["argument"]
            if o["evidence"]:
                body += "\n\nEvidence:\n- " + "\n- ".join(o["evidence"])
            _print(f"OPPONENT -- Round {i + 1}", body, style="red")

        if i < len(state["judge_history"]):
            j = state["judge_history"][i]
            body = (
                f"Advocate scores: {j['advocate_scores']}\n"
                f"Opponent scores: {j['opponent_scores']}\n\n"
                f"Advocate weaknesses: {j['advocate_weaknesses']}\n"
                f"Opponent weaknesses: {j['opponent_weaknesses']}\n\n"
                f"Round winner: {j['winner']}\n"
                f"Needs more evidence: {j['needs_more_evidence']}"
                + (f" (requested from: {j['evidence_requested_from']})" if j["needs_more_evidence"] else "")
                + f"\n\nSummary: {j['summary']}"
            )
            _print(f"JUDGE -- Round {i + 1}", body, style="yellow")

    fv = state.get("final_verdict")
    if fv:
        body = (
            f"VERDICT: {str(fv.get('verdict', '?')).upper()}\n"
            f"Confidence: {fv.get('confidence', '?')}/10\n\n"
            "Key deciding factors:\n- " + "\n- ".join(fv.get("key_deciding_factors", []))
            + "\n\nReasoning:\n" + fv.get("reasoning", "")
        )
        _print("FINAL VERDICT", body, style="bold magenta")

def save_state(state: dict, path: str) -> None:
    with open(path, "w") as f:
        json.dump(state, f, indent=2)

def main() -> None:
    parser = argparse.ArgumentParser(description="Debate Court -- adversarial LangGraph system")
    parser.add_argument(
        "claim",
        nargs="?",
        default="Open-source LLMs will surpass proprietary models.",
        help="The controversial claim to debate.",
    )
    parser.add_argument("--max-rounds", type=int, default=MAX_ROUNDS_DEFAULT)
    parser.add_argument(
        "--inject-evidence",
        type=str,
        default=None,
        help="New evidence to inject into a second run, to test if the verdict flips.",
    )
    parser.add_argument(
        "--inject-side",
        type=str,
        default="both",
        choices=["advocate", "opponent", "both"],
        help="Which side receives the injected evidence.",
    )
    parser.add_argument("--out", type=str, default=None, help="Path to save the transcript as JSON.")
    args = parser.parse_args()

    print(f"\nRunning debate on: {args.claim}\n")
    state1 = run_debate(args.claim, max_rounds=args.max_rounds)
    print_transcript(state1)

    if args.out:
        save_state(state1, args.out)
        print(f"\nSaved transcript to {args.out}")

    if args.inject_evidence:
        print("\n\n" + "=" * 70)
        print("RE-RUNNING DEBATE WITH NEW EVIDENCE INJECTED")
        print("=" * 70)
        state2 = run_debate(
            args.claim,
            max_rounds=args.max_rounds,
            injected_evidence=args.inject_evidence,
            injected_evidence_side=args.inject_side,
        )
        print_transcript(state2)

        v1 = (state1.get("final_verdict") or {}).get("verdict")
        v2 = (state2.get("final_verdict") or {}).get("verdict")
        print(f"\n\nVERDICT WITHOUT NEW EVIDENCE: {v1}")
        print(f"VERDICT WITH NEW EVIDENCE:    {v2}")
        print("--> VERDICT CHANGED" if v1 != v2 else "--> Verdict unchanged")

        if args.out:
            out2 = args.out.rsplit(".", 1)[0] + "_with_evidence.json"
            save_state(state2, out2)
            print(f"Saved second transcript to {out2}")

if __name__ == "__main__":
    main()