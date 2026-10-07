"""
Legacy benchmark module retained only for historical comparison.

Production HeedX functionality uses the qualitative analysis engine,
conversation state manager, safety layer, and RAG engine instead of the
old classification-based assessment pipeline.
"""

# Intentionally left in place for compatibility with older scripts and
# research benchmarking, but it is no longer used in the active app flow.

import pandas as pd
import numpy as np
from collections import Counter
import re
from .preprocessing import preprocess_text, split_sentences
from .lexicons import (
    INTENSITY_KEYWORDS, RESILIENCE_KEYWORDS, CRISIS_TRIGGERS,
    NEGATIONS, WELLNESS_KEYWORDS
)
from config.settings import RISK_THRESHOLDS


class MentalHealthAnalyzer:
    """Deprecated legacy analyzer. Not used by the active migratable app."""

    def __init__(self, model, classes):
        self.model = model
        self.classes = classes
        self.sentence_predictions = []
        self.aggregated_results = {}
        self.intensity_keywords = INTENSITY_KEYWORDS
        self.resilience_keywords = RESILIENCE_KEYWORDS
        self.crisis_triggers = CRISIS_TRIGGERS
        self.negations = NEGATIONS
        self.wellness_keywords = WELLNESS_KEYWORDS
        self.classes_list = list(self.classes)
        self.thresholds = RISK_THRESHOLDS

    def _is_target_negated(self, target_pattern, text, window=3):
        return False

    def _detect_negated_wellness(self, text, window=3):
        return False

    def _detect_negated_distress(self, text, window=3):
        return False

    def _evaluate_crisis_intent(self, cleaned_text):
        return False, False, False

    def _calculate_intensity(self, sentence):
        return 1.0

    def _detect_resilience(self, sentence):
        return False

    def analyze_response(self, text, question_id=None):
        return []

    def analyze_all_responses(self, responses_dict):
        return []

    def _extract_markers(self, sentence, actual_crisis_intent=False, is_crisis_negated=False, is_negated_wellness=False):
        return []

    def _aggregate_predictions(self):
        return {}

    def get_risk_level(self):
        return "unknown"

    def get_suicidal_flagged_sentences(self):
        return []


def create_distribution_dataframe(distribution):
    df = pd.DataFrame({
        'Mental Health Indicator': list(distribution.keys()),
        'Percentage': list(distribution.values())
    })
    return df.sort_values('Percentage', ascending=False)

