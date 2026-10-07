"""
HeedX AI — Conversation State Manager
Maintains and evolves a structured multi-turn conversation state.
Tracks accumulated concerns, duration, stressors, functional impact, and safety signals.
Generates targeted retrieval queries rather than blindly concatenating entire transcripts.
"""

from typing import Dict, List, Any, Optional
from .qualitative_engine import QualitativeAnalysisEngine
from .safety_layer import SafetyLayer


class ConversationStateManager:
    """
    State Manager for Conversational User Mode.
    Accumulates user signals turn-by-turn to support grounded, context-aware dialogue.
    """

    def __init__(self):
        self.state = {
            "main_concerns": [],
            "duration": None,
            "stressors": [],
            "functional_impact": [],
            "risk_signals": [],
            "risk_status": "not_established"
        }
        self.history: List[Dict[str, str]] = []
        self.turn_count: int = 0

    def update_state(
        self,
        user_message: str,
        qualitative_engine: QualitativeAnalysisEngine,
        safety_layer: Optional[SafetyLayer] = None
    ) -> Dict[str, Any]:
        """
        Updates the conversation state with information extracted from the latest turn.
        """
        self.turn_count += 1
        analysis = qualitative_engine.analyze(user_message)

        # 1. Accumulate main concerns
        new_concerns = analysis.get("presenting_concerns", [])
        for c in new_concerns:
            if c != "general distress / unclassified concerns" and c not in self.state["main_concerns"]:
                self.state["main_concerns"].append(c)

        # 2. Also incorporate symptom signals into main concerns
        for s in analysis.get("symptoms_or_signals", []):
            if s != "unspecified emotional or physical strain" and s not in self.state["main_concerns"]:
                self.state["main_concerns"].append(s)

        # 3. Update duration if stated
        extracted_duration = analysis.get("duration")
        if extracted_duration and "not explicitly stated" not in extracted_duration:
            self.state["duration"] = extracted_duration

        # 4. Accumulate stressors
        for stress in analysis.get("stressors", []):
            if stress not in self.state["stressors"]:
                self.state["stressors"].append(stress)

        # 5. Accumulate functional impact
        for impact in analysis.get("functional_impact", []):
            if impact not in self.state["functional_impact"]:
                self.state["functional_impact"].append(impact)

        # 6. Evaluate safety
        if safety_layer:
            safety_eval = safety_layer.evaluate_message(user_message)
            if safety_eval.get("is_crisis"):
                self.state["risk_status"] = "acute_crisis"
                for trig in safety_eval.get("matched_triggers", []):
                    if trig not in self.state["risk_signals"]:
                        self.state["risk_signals"].append(trig)
            elif safety_eval.get("is_negated_crisis"):
                if self.state["risk_status"] != "acute_crisis":
                    self.state["risk_status"] = "safe_negated"

        return self.get_state_dict()

    def get_state_dict(self) -> Dict[str, Any]:
        """Returns the current state dictionary"""
        return {
            "main_concerns": list(self.state["main_concerns"]),
            "duration": self.state["duration"] or "not established",
            "stressors": list(self.state["stressors"]),
            "functional_impact": list(self.state["functional_impact"]),
            "risk_signals": list(self.state["risk_signals"]),
            "risk_status": self.state["risk_status"]
        }

    def build_retrieval_query(self, current_message: str) -> str:
        """
        Constructs a focused retrieval query combining the current turn's text
        with accumulated high-signal state items.
        """
        terms = []
        # Current message content
        terms.append(current_message.strip())

        # Active state signals
        if self.state["main_concerns"]:
            terms.extend(self.state["main_concerns"][:3])
        if self.state["stressors"]:
            terms.extend(self.state["stressors"][:2])

        # Avoid unbounded length
        deduped = []
        seen = set()
        for t in terms:
            w = t.lower()
            if w not in seen:
                seen.add(w)
                deduped.append(t)

        return " ".join(deduped[:8])

    get_retrieval_query = build_retrieval_query

    def format_state_for_prompt(self) -> str:
        """Formats the current conversation state for inclusion in the LLM system prompt"""
        state = self.get_state_dict()
        lines = ["CURRENT CONVERSATION STATE (Continuously tracked across turns):"]
        lines.append(f"- Main concerns identified: {', '.join(state['main_concerns']) if state['main_concerns'] else 'None specifically identified yet'}")
        lines.append(f"- Duration: {state['duration']}")
        lines.append(f"- Context & Stressors: {', '.join(state['stressors']) if state['stressors'] else 'None established'}")
        lines.append(f"- Functional impact: {', '.join(state['functional_impact']) if state['functional_impact'] else 'None reported'}")
        lines.append(f"- Risk status: {state['risk_status'].upper()}")
        return "\n".join(lines)

    def add_turn(self, role: str, content: str):
        """Records a completed turn in history"""
        self.history.append({"role": role, "content": content})

    def clear(self):
        """Resets the conversation state"""
        self.state = {
            "main_concerns": [],
            "duration": None,
            "stressors": [],
            "functional_impact": [],
            "risk_signals": [],
            "risk_status": "not_established"
        }
        self.history = []
        self.turn_count = 0
