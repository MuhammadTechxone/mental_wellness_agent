"""
Core analysis engine: sentence-level prediction and aggregation
"""

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
    """
    Evolved Analysis Engine: Incorporates Sentiment, Intensity, Negation, 
    and Hybrid Rule-Based Safety logic.
    """
    
    def __init__(self, model, classes):
        """
        Initialize with loaded pipeline model
        """
        self.model = model
        self.classes = classes
        self.sentence_predictions = []
        self.aggregated_results = {}
        
        # Intensity and Crisis Lexicons for Explainable AI
        self.intensity_keywords = INTENSITY_KEYWORDS
        self.resilience_keywords = RESILIENCE_KEYWORDS
        self.crisis_triggers = CRISIS_TRIGGERS
        self.negations = NEGATIONS
        self.wellness_keywords = WELLNESS_KEYWORDS
        self.classes_list = list(self.classes)
        self.thresholds = RISK_THRESHOLDS

    def _is_target_negated(self, target_pattern, text, window=3):
        """
        Determines whether a specific target pattern is actively negated
        by checking a local window of words immediately preceding its occurrence.
        Avoids global false-negatives across compound sentences.
        """
        if not text:
            return False
            
        for match in re.finditer(target_pattern, text, re.IGNORECASE):
            start_pos = match.start()
            preceding_text = text[:start_pos].strip()
            if not preceding_text:
                continue
                
            preceding_words = preceding_text.split()
            check_words = preceding_words[-window:]
            
            # Check for direct negation words or negation phrases ('no longer', etc.)
            if any(w in self.negations for w in check_words):
                return True
            if "no" in check_words and "longer" in check_words:
                return True
            if "free" in check_words and "from" in check_words:
                return True
                
        return False

    def _detect_negated_wellness(self, text, window=3):
        """
        Detects if positive wellness terms (e.g. 'fine', 'okay', 'good', 'happy')
        are directly preceded by negation words (e.g. 'not okay', 'never fine').
        """
        for well in self.wellness_keywords:
            pattern = r'\b' + re.escape(well) + r'\b'
            if self._is_target_negated(pattern, text, window=window):
                return True
        return False

    def _detect_negated_distress(self, text, window=3):
        """
        Detects if clinical distress words (e.g. 'depressed', 'anxious')
        are directly preceded by negation words (e.g. 'not depressed', 'not anxious').
        """
        distress_words = [
            'depressed', 'depression', 'sad', 'sadness', 'anxious', 'anxiety',
            'worried', 'hopeless', 'stressed', 'panic', 'suicidal', 'suicide'
        ]
        for term in distress_words:
            pattern = r'\b' + re.escape(term) + r'\b'
            if self._is_target_negated(pattern, text, window=window):
                return True
        return False

    def _evaluate_crisis_intent(self, cleaned_text):
        """
        Evaluates whether crisis triggers are present and whether they are negated.
        Returns:
            has_crisis: bool (any crisis pattern found)
            is_negated: bool (all found crisis patterns are explicitly negated)
            actual_intent: bool (crisis pattern is present AND NOT negated)
        """
        found_triggers = []
        for pattern in self.crisis_triggers:
            if re.search(pattern, cleaned_text, re.IGNORECASE):
                found_triggers.append(pattern)
                
        if not found_triggers:
            return False, False, False
            
        unnegated_triggers = []
        for pattern in found_triggers:
            if not self._is_target_negated(pattern, cleaned_text, window=3):
                unnegated_triggers.append(pattern)
                
        has_crisis = True
        actual_intent = len(unnegated_triggers) > 0
        is_negated = not actual_intent
        
        return has_crisis, is_negated, actual_intent

    def _calculate_intensity(self, sentence):
        """Calculates emotional intensity based on modifiers"""
        score = 1.0
        words = preprocess_text(sentence).split()
        for word in words:
            if word in self.intensity_keywords['high']: score += 0.5
            if word in self.intensity_keywords['moderate']: score += 0.2
        return min(score, 2.5) # Cap intensity multiplier

    def _detect_resilience(self, sentence):
        """Detects if the user is expressing hope or recovery intent"""
        words = preprocess_text(sentence).split()
        return any(word in words for word in self.resilience_keywords)
        
    def analyze_response(self, text, question_id=None):
        """
        Analyze a single response by breaking into sentences
        Returns list of sentence-level predictions with scope-aware negation and safety.
        """
        if not text:
            return []
        
        # Split into sentences
        sentences = split_sentences(text)
        results = []
        
        for sentence in sentences:
            if len(sentence.split()) < 2:  # Skip very short sentences
                continue
            
            # 1. Preprocessing & ML Classification
            cleaned = preprocess_text(sentence)
            prediction = self.model.predict([cleaned])[0]
            
            # 2. Scope-Aware Hybrid Safety Analysis
            has_crisis, is_crisis_negated, actual_crisis_intent = self._evaluate_crisis_intent(cleaned)
            is_negated_wellness = self._detect_negated_wellness(cleaned)
            is_negated_distress = self._detect_negated_distress(cleaned)
            intensity = self._calculate_intensity(sentence)
            has_resilience = self._detect_resilience(sentence)
            
            # 3. Prediction confidence estimation
            try:
                decision_scores = self.model.decision_function([cleaned])[0]
                exp_scores = np.exp(decision_scores - np.max(decision_scores))
                probs = exp_scores / exp_scores.sum()
                confidence = probs[self.classes_list.index(prediction)]
            except:
                confidence = None
            
            # 4. Scope-Aware Logic Adjustments (Controlled Intelligence)
            if actual_crisis_intent:
                # Active crisis trigger verified and NOT negated:
                # Immediate override to 'suicidal'
                prediction = 'suicidal'
                confidence = max(confidence or 0.5, 0.95)
                
            elif is_crisis_negated:
                # User explicitly negated suicidal ideation ("not suicidal", "don't want to die")
                if prediction == 'suicidal':
                    prediction = 'normal'
                    confidence = 0.85
                    
            elif is_negated_wellness:
                # "not okay", "not fine", "never happy"
                # If model classified as normal, force to depression/distress
                if prediction == 'normal':
                    prediction = 'depression'
                    confidence = max(confidence or 0.5, 0.70)
                    
            elif is_negated_distress:
                # User explicitly negated distress ("not depressed", "not feeling anxious")
                if prediction in ['depression', 'anxiety']:
                    prediction = 'normal'
                    confidence = max(confidence or 0.5, 0.75)

            # Resilience Offset: If expressing recovery/hope, gently balance distress confidence
            if has_resilience and prediction in ['depression', 'anxiety']:
                if confidence:
                    confidence *= 0.85

            results.append({
                'sentence': sentence,
                'prediction': prediction,
                'confidence': confidence,
                'intensity': intensity,
                'has_negation': is_crisis_negated or is_negated_wellness or is_negated_distress,
                'is_crisis_rule': actual_crisis_intent,
                'question_id': question_id,
                'markers': self._extract_markers(
                    sentence, 
                    actual_crisis_intent=actual_crisis_intent,
                    is_crisis_negated=is_crisis_negated,
                    is_negated_wellness=is_negated_wellness
                ),
                'is_resilient': has_resilience
            })
        
        return results
    
    def analyze_all_responses(self, responses_dict):
        """
        Analyze all questionnaire responses
        responses_dict: {question_id: response_text}
        """
        all_predictions = []
        
        for q_id, response in responses_dict.items():
            if response and response.strip():
                sentence_results = self.analyze_response(response, q_id)
                all_predictions.extend(sentence_results)
        
        self.sentence_predictions = all_predictions
        self.aggregated_results = self._aggregate_predictions()
        
        return self.sentence_predictions
    
        
    def _extract_markers(self, sentence, actual_crisis_intent=False, is_crisis_negated=False, is_negated_wellness=False):
        """Extracts explainable signals for the UI"""
        cleaned = preprocess_text(sentence)
        words = cleaned.split()
        
        found = []
        if actual_crisis_intent:
            found.append("crisis-intent")
        elif is_crisis_negated:
            found.append("negated-crisis")
            
        if is_negated_wellness or (any(neg in words for neg in self.negations) and any(well in words for well in self.wellness_keywords)):
            found.append("negated-wellness")
            
        found += [w for w in words if any(w in l for l in self.intensity_keywords.values())]
        found += [w for w in words if w in self.resilience_keywords]
        return list(dict.fromkeys(found))[:3] # Remove duplicates while keeping order

    


    def _aggregate_predictions(self):
        """
        Advanced Aggregation: Uses weighted scores based on intensity and confidence
        """
        if not self.sentence_predictions:
            return {}
        
        total = len(self.sentence_predictions)

        # Weighted Aggregation Logic
        weighted_scores = {cls: 0.0 for cls in self.classes}
        
        for p in self.sentence_predictions:
            # Weight = Confidence * Intensity
            weight = (p['confidence'] or 0.5) * p['intensity']
            weighted_scores[p['prediction']] += weight
            
        total_weight = sum(weighted_scores.values())

        # Safety check: avoid division by zero
        if total_weight == 0:
            weighted_scores['normal'] = 1.0
            total_weight = 1.0
        
        # Calculate percentages
        distribution = {}
        for class_name in self.classes:
            distribution[class_name] = (weighted_scores[class_name] / total_weight * 100) if total_weight > 0 else 0
        
        # Find primary and secondary indicators
        sorted_classes = sorted(distribution.items(), key=lambda x: x[1], reverse=True)

        # Contextual Continuity Logic: Detect if risk is escalating
        escalation = False
        if len(self.sentence_predictions) > 3:
            # Check if latter half of sentences have higher distress than first half
            half = len(self.sentence_predictions) // 2
            first_half_distress = sum(1 for p in self.sentence_predictions[:half] if p['prediction'] != 'normal')
            second_half_distress = sum(1 for p in self.sentence_predictions[half:] if p['prediction'] != 'normal')
            if second_half_distress > first_half_distress:
                escalation = True
        
        result = {
            'total_sentences': total,
            'distribution': distribution,
            'primary_indicator': sorted_classes[0][0] if sorted_classes else None,
            'primary_percentage': sorted_classes[0][1] if sorted_classes else 0,
            'secondary_indicator': sorted_classes[1][0] if len(sorted_classes) > 1 else None,
            'secondary_percentage': sorted_classes[1][1] if len(sorted_classes) > 1 else 0,
            'raw_predictions': self.sentence_predictions,
            'continuity': {
                'escalating_distress': escalation,
                'resilience_count': sum(1 for p in self.sentence_predictions if p['is_resilient'])
            }
        }
        
        return result
    
    def get_risk_level(self):
        """
        Determine risk level based on aggregated predictions
        """
        if not self.aggregated_results:
            return "unknown"
        
        dist = self.aggregated_results['distribution']
        suicidal_pct = dist.get('suicidal', 0)
        
        # Base Risk Level
        risk_level = "mild"
        
        # High intensity suicidal indicators trigger high risk immediately
        if suicidal_pct >= self.thresholds['suicidal_high_risk'] or \
           any(p['is_crisis_rule'] for p in self.sentence_predictions):
            risk_level = "high"
        elif suicidal_pct >= self.thresholds['suicidal_moderate']:
            risk_level = "moderate_high"
        elif (dist.get('depression', 0) + dist.get('anxiety', 0)) >= self.thresholds['depression_anxiety_threshold']:
            risk_level = "moderate"
        elif dist.get('normal', 0) >= 60:
            risk_level = "low"
            
        # Contextual Escalation Adjustment: Promote risk if distress is growing
        if self.aggregated_results.get('continuity', {}).get('escalating_distress'):
            if risk_level == "moderate": risk_level = "moderate_high"
            elif risk_level == "mild": risk_level = "moderate"
            
        return risk_level
    
    def get_suicidal_flagged_sentences(self):
        """
        Return all sentences flagged as suicidal for review
        """
        if not self.sentence_predictions:
            return []
        
        return [p for p in self.sentence_predictions if p['prediction'] == 'suicidal']


def create_distribution_dataframe(distribution):
    """
    Create a formatted DataFrame for visualization
    """
    df = pd.DataFrame({
        'Mental Health Indicator': list(distribution.keys()),
        'Percentage': list(distribution.values())
    })
    return df.sort_values('Percentage', ascending=False)