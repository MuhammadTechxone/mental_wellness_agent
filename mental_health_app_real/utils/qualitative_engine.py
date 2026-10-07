"""
HeedX AI — Qualitative Analysis Engine
Extracts structured qualitative clinical dimensions from text:
presenting_concerns, symptoms_or_signals, emotions, stressors,
duration, functional_impact, social_context, protective_factors,
risk_signals, support_needs, uncertainties.

Prioritizes factual representation and semantic interpretation over
synthetic diagnostic percentages.
"""

import re
from typing import Dict, List, Any, Optional
from .lexicons import NIGERIAN_IDIOM_MAP, CRISIS_TRIGGERS, RESILIENCE_KEYWORDS, NEGATIONS


class QualitativeAnalysisEngine:
    """
    Qualitative Analysis Engine for HeedX AI.
    Analyzes patient/client text or user conversation turns
    and generates structured qualitative clinical information.
    """

    def __init__(self):
        # Clinical concept dictionaries for deterministic/rule semantic detection
        self.symptom_patterns = {
            "low_mood": [
                r"\b(sad|sadness|unhappy|down|feeling low|spirit is low|no joy|spirit weak|depressed|depression)\b"
            ],
            "sleep_disturbance": [
                r"\b(sleep difficulty|difficulty sleeping|insomnia|can't sleep|cannot sleep|trouble sleeping|hard to sleep|waking up early|nightmare|barely sleep|poor sleep)\b"
            ],
            "anhedonia": [
                r"\b(loss of interest|stopped enjoying|no vibe|vibe finish|don't enjoy|not enjoying|lost interest|nothing excites|loss of pleasure)\b"
            ],
            "social_withdrawal": [
                r"\b(withdrawn|withdrawing|withdrawn from friends|isolating|isolation|avoiding people|stopped seeing friends|stopped enjoying social activities|social withdrawal|avoiding social|stay in room|alone)\b"
            ],
            "concentration_difficulty": [
                r"\b(difficulty concentrating|can't focus|cannot concentrate|struggling to concentrate|mind wandering|brain fog)\b"
            ],
            "fatigue_low_energy": [
                r"\b(fatigue|exhausted|no get power|tired|taya|body no be firewood|weak|drained|no energy)\b"
            ],
            "anxiety_panic": [
                r"\b(anxiety|anxious|panic|heart racing|heart is cutting|chest tight|nervous|worry|worried|tension|head is hot)\b"
            ],
            "hopelessness": [
                r"\b(hopeless|no hope|no point|what's the use|what is the use|useless|worthless)\b"
            ]
        }

        self.stressor_patterns = {
            "academic_stress": [
                r"\b(university|school|exam|exams|academic|classes|coursework|lecturer|grades|cgpa|faculty|polytechnic|hostel|academic workload)\b"
            ],
            "financial_stress": [
                r"\b(money|financial|fees|rent|broke|no funds|poverty|debt|feeding|transport fare)\b"
            ],
            "career_unemployment": [
                r"\b(job|work|unemployed|unemployment|career|boss|salary|seeking employment)\b"
            ],
            "relationship_family": [
                r"\b(parents|father|mother|family|boyfriend|girlfriend|husband|wife|marriage|partner|breakup|divorce)\b"
            ],
            "health_grief": [
                r"\b(illness|sick|hospital|death|died|lost someone|grief|bereavement|funeral)\b"
            ]
        }

        self.duration_regex = [
            r"(\b(?:for\s+)?(?:the\s+)?(?:past|last|about|approximately|almost|over)\s+(?:\d+|one|two|three|four|five|six|several|a few|a|an)?\s*(?:days?|weeks?|months?|years?)\b)",
            r"(\b(?:for|over|about|approximately)\s+(?:\d+|one|two|three|four|five|six|several|a few|a)\s+(?:days?|weeks?|months?|years?)\b)",
            r"(\b(?:one|two|three|four|five|six|\d+)\s+(?:month|week|year|day)s?\b)",
            r"(\bfor\s+(?:a|some)\s+(?:while|time|days|weeks|months)\b)"
        ]

    def _extract_duration(self, text: str) -> Optional[str]:
        """Extracts temporal duration statements from text"""
        for pat in self.duration_regex:
            match = re.search(pat, text, re.IGNORECASE)
            if match:
                return match.group(0).strip()
        return None

    def _is_negated(self, pattern: str, text: str, window: int = 4) -> bool:
        """Determines if a matched clinical term is negated within local context"""
        for match in re.finditer(pattern, text, re.IGNORECASE):
            start = match.start()
            preceding_words = text[:start].strip().split()[-window:]
            if any(neg in preceding_words for neg in NEGATIONS):
                return True
        return False

    def analyze(self, text: str) -> Dict[str, Any]:
        """
        Performs qualitative analysis on the supplied text,
        producing a structured clinical representation.
        """
        if not text or not isinstance(text, str):
            text = ""

        cleaned = text.strip()
        lower_text = cleaned.lower()

        # Translate Nigerian idioms for semantic awareness
        idiom_translated = lower_text
        for idiom, repl in NIGERIAN_IDIOM_MAP.items():
            idiom_translated = idiom_translated.replace(idiom, repl)

        # 1. Duration extraction
        duration = self._extract_duration(cleaned)

        # 2. Symptoms & Signals Extraction
        symptoms = []
        concerns = []
        emotions = []

        for category, patterns in self.symptom_patterns.items():
            for pat in patterns:
                if re.search(pat, lower_text) or re.search(pat, idiom_translated):
                    if not self._is_negated(pat, lower_text) and not self._is_negated(pat, idiom_translated):
                        cat_label = category.replace("_", " ")
                        if category in ["low_mood", "hopelessness"]:
                            if "persistent sadness" not in concerns and "low mood" not in concerns:
                                concerns.append("persistent sadness" if duration else "low mood")
                            emotions.append("sad" if category == "low_mood" else "discouraged")
                        elif category == "sleep_disturbance":
                            symptoms.append("sleep difficulty")
                            if "sleep difficulty" not in concerns:
                                concerns.append("sleep difficulty")
                        elif category == "anhedonia":
                            symptoms.append("reduced interest / loss of enjoyment")
                            if "reduced interest / loss of enjoyment" not in concerns:
                                concerns.append("reduced interest / loss of enjoyment")
                        elif category == "social_withdrawal":
                            symptoms.append("social withdrawal")
                            if "social withdrawal" not in concerns:
                                concerns.append("social withdrawal")
                        elif category == "concentration_difficulty":
                            symptoms.append("difficulty concentrating")
                        elif category == "fatigue_low_energy":
                            symptoms.append("low energy / fatigue")
                        elif category == "anxiety_panic":
                            symptoms.append("anxiety / somatic tension")
                            concerns.append("anxiety")
                            emotions.append("anxious / overwhelmed")
                        break

        # 3. Stressors & Context Extraction
        stressors = []
        social_context = []

        for category, patterns in self.stressor_patterns.items():
            for pat in patterns:
                if re.search(pat, lower_text):
                    if category == "academic_stress":
                        stressors.append("academic workload / university pressure")
                        social_context.append("university/academic environment")
                    elif category == "financial_stress":
                        stressors.append("financial hardship / economic stress")
                    elif category == "career_unemployment":
                        stressors.append("work / career uncertainty")
                    elif category == "relationship_family":
                        stressors.append("family or interpersonal strain")
                    elif category == "health_grief":
                        stressors.append("health issues or bereavement")
                    break

        # 4. Functional Impact Extraction
        functional_impact = []
        if "difficulty concentrating" in symptoms:
            functional_impact.append("academic or cognitive task concentration")
        if re.search(r"\b(struggling at university|failing|cannot study|miss classes|can't work|cannot work)\b", lower_text):
            functional_impact.append("academic/occupational performance")
        if "social withdrawal" in symptoms:
            functional_impact.append("social relationships and engagement")

        # 5. Protective Factors & Resilience
        protective_factors = []
        for word in RESILIENCE_KEYWORDS:
            if re.search(r'\b' + re.escape(word) + r'\b', lower_text):
                if not self._is_negated(r'\b' + re.escape(word) + r'\b', lower_text):
                    protective_factors.append(f"expressed coping / {word}")
        if re.search(r"\b(pray|church|mosque|god|faith|pastor|imam)\b", lower_text):
            protective_factors.append("spiritual or faith-based coping framework")
        if re.search(r"\b(family|friend|friends|sister|brother|mother|father)\b", lower_text):
            if "family or interpersonal strain" not in stressors:
                protective_factors.append("presence of family/friend support network")

        # 6. Risk Signals & Safety Triage
        risk_signals = []
        uncertainties = []

        for trig in CRISIS_TRIGGERS:
            if re.search(trig, lower_text):
                if self._is_negated(trig, lower_text):
                    uncertainties.append(f"suicidal ideation explicitly negated in context ('{trig}')")
                else:
                    risk_signals.append(f"acute risk language detected: '{trig}'")

        if not risk_signals:
            uncertainties.append("no suicidal ideation established from the supplied text")
            uncertainties.append("further longitudinal assessment may be appropriate")

        # Fallback deduplication
        concerns = list(dict.fromkeys(concerns))
        symptoms = list(dict.fromkeys(symptoms))
        emotions = list(dict.fromkeys(emotions))
        stressors = list(dict.fromkeys(stressors))
        functional_impact = list(dict.fromkeys(functional_impact))
        protective_factors = list(dict.fromkeys(protective_factors))
        risk_signals = list(dict.fromkeys(risk_signals))
        uncertainties = list(dict.fromkeys(uncertainties))

        return {
            "presenting_concerns": concerns if concerns else ["general distress / unclassified concerns"],
            "emotions": emotions if emotions else ["distressed"],
            "symptoms_or_signals": symptoms if symptoms else ["unspecified emotional or physical strain"],
            "stressors": stressors,
            "duration": duration or "duration not explicitly stated in supplied text",
            "functional_impact": functional_impact,
            "social_context": social_context,
            "protective_factors": protective_factors,
            "risk_signals": risk_signals,
            "support_needs": [
                "evidence-grounded psychoeducation",
                "supportive listening and coping exploration"
            ],
            "uncertainties": uncertainties
        }

    def format_for_display(self, analysis: Dict[str, Any]) -> str:
        """
        Formats qualitative clinical analysis into clear, professional Markdown,
        strictly avoiding synthetic diagnostic percentages.
        """
        md = []
        md.append("### Qualitative Case Extraction\n")

        md.append("**Presenting concerns**")
        for c in analysis.get("presenting_concerns", []):
            md.append(f"• {c}")
        md.append("")

        md.append("**Duration**")
        md.append(f"• {analysis.get('duration', 'Not established')}\n")

        if analysis.get("stressors") or analysis.get("social_context"):
            md.append("**Context & Stressors**")
            for s in analysis.get("stressors", []):
                md.append(f"• {s}")
            for sc in analysis.get("social_context", []):
                md.append(f"• Context: {sc}")
            md.append("")

        md.append("**Potentially relevant symptoms/signals**")
        for s in analysis.get("symptoms_or_signals", []):
            md.append(f"• {s}")
        md.append("")

        if analysis.get("functional_impact"):
            md.append("**Functional impact**")
            for f in analysis.get("functional_impact", []):
                md.append(f"• {f}")
            md.append("")

        if analysis.get("protective_factors"):
            md.append("**Observed protective factors / strengths**")
            for p in analysis.get("protective_factors", []):
                md.append(f"• {p}")
            md.append("")

        md.append("**Risk & Safety information**")
        if analysis.get("risk_signals"):
            for r in analysis.get("risk_signals"):
                md.append(f"⚠️ **ACTIVE RISK SIGNAL**: {r}")
        else:
            md.append("• No explicit acute crisis or suicidal ideation established from supplied text")
        for u in analysis.get("uncertainties", []):
            if "no suicidal ideation" not in u:
                md.append(f"• *Clinical note:* {u}")

        return "\n".join(md)
