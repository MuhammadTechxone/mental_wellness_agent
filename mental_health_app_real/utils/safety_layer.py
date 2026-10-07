"""
HeedX AI — Dedicated Safety Layer
Provides rule-based, explicit safety triage and crisis protocols.
Operates independently from standard RAG retrieval and LLM generation.
"""

import re
from typing import Dict, Any, List, Optional
from config.settings import NIGERIA_EMERGENCY_NUMBERS, MENTAL_HEALTH_SUPPORT, PROFESSIONAL_HELP
from .lexicons import CRISIS_TRIGGERS, NEGATIONS


class SafetyLayer:
    """
    Explicit Safety & Crisis Intercept Layer.
    Guarantees immediate clinical guardrails, crisis de-escalation,
    and verified Nigerian emergency resources for at-risk users.
    """

    def __init__(self):
        self.crisis_triggers = CRISIS_TRIGGERS
        self.negations = NEGATIONS

    def _is_negated(self, pattern: str, text: str, window: int = 3) -> bool:
        """Checks if a crisis pattern is negated within a local word window"""
        for match in re.finditer(pattern, text, re.IGNORECASE):
            start = match.start()
            preceding_words = text[:start].strip().split()[-window:]
            if any(w in self.negations for w in preceding_words):
                return True
            if "no" in preceding_words and "longer" in preceding_words:
                return True
        return False

    def evaluate_message(self, text: str) -> Dict[str, Any]:
        """
        Evaluates a user message or clinical observation for safety risks.
        Returns safety assessment, crisis flags, and deterministic crisis responses.
        """
        if not text or not isinstance(text, str):
            return {
                "is_crisis": False,
                "is_negated_crisis": False,
                "risk_level": "none",
                "matched_triggers": [],
                "emergency_response": None
            }

        cleaned = text.strip().lower()
        active_triggers = []
        negated_triggers = []

        for pattern in self.crisis_triggers:
            if re.search(pattern, cleaned, re.IGNORECASE):
                if self._is_negated(pattern, cleaned):
                    negated_triggers.append(pattern)
                else:
                    active_triggers.append(pattern)

        if active_triggers:
            emergency_message = self._build_emergency_response()
            return {
                "is_crisis": True,
                "is_negated_crisis": False,
                "risk_level": "acute_crisis",
                "matched_triggers": active_triggers,
                "emergency_response": emergency_message
            }
        elif negated_triggers:
            return {
                "is_crisis": False,
                "is_negated_crisis": True,
                "risk_level": "safe_negated",
                "matched_triggers": negated_triggers,
                "emergency_response": None
            }

        return {
            "is_crisis": False,
            "is_negated_crisis": False,
            "risk_level": "standard",
            "matched_triggers": [],
            "emergency_response": None
        }

    def _build_emergency_response(self) -> str:
        """Constructs immediate, empathetic, verified crisis support instructions"""
        return (
            "### 🚨 Immediate Safety Support Required\n\n"
            "What you have just shared indicates that you may be in severe emotional pain or experiencing thoughts of harm. "
            "Your life has immense value, and you do not have to carry this alone. Please connect with immediate help right now:\n\n"
            "**Verified Nigerian Emergency & Crisis Hotlines (24/7, Confidential):**\n"
            "- **National Emergency:** Call **112** (toll-free across all Nigerian networks)\n"
            "- **Mentally Aware Nigeria Initiative (MANI):** **08062106493** or **08139136621**\n"
            "- **She Writes Woman (Mental Health Crisis Support):** **08099769974**\n"
            "- **Nigerian Suicide Prevention Helpline:** **08099696969**\n\n"
            "**Walk-in Psychiatric Emergency:**\n"
            "You can walk into the emergency unit of any Federal Neuropsychiatric Hospital (Yaba-Lagos, Aro-Abeokuta, Kaduna, Benin, Maiduguri) "
            "or the nearest University Teaching Hospital (LUTH, UCH, UNN, ABU) at any time of day or night.\n\n"
            "Please reach out to a trusted loved one, family member, or professional right away. We are here with you."
        )
