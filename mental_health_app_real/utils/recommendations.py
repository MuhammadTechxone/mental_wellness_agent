"""
Recommendation engine based on risk assessment
"""

from config.settings import RECOMMENDATIONS


class RecommendationEngine:
    """
    Provides appropriate recommendations based on analysis results
    """
    
    def __init__(self):
        self.recommendations = RECOMMENDATIONS
    
    def get_recommendations(self, primary_indicator, risk_level, suicidal_flagged=None):
        """
        Get tailored recommendations based on primary indicator and risk level
        """
        # Handle high-risk suicidal cases first
        if risk_level in ['high', 'moderate_high'] and suicidal_flagged:
            return self.recommendations['suicidal']
        
        # Get recommendations based on primary indicator
        if primary_indicator in self.recommendations:
            return self.recommendations[primary_indicator]
        
        # Default to normal if unknown
        return self.recommendations['normal']
    
    def get_crisis_resources(self):
        """
        Return crisis resources for high-risk situations
        """
        return {
            'title': "🚨 Crisis Resources",
            'resources': [
                "**National Emergency Services:** Call 112",
                "**Mentally Aware Nigeria Initiative (MANI):** 08062106493",
                "**She Writes Woman:** 08099769974",
                "**Lagos State Help Line:** 767 or 112"
            ],
            'message': "These resources provide immediate, confidential support 24/7."
        }
    
    def get_qualitative_recommendations(self, analysis_dict: dict) -> dict:
        """
        Generate evidence-informed coping and support guidance based on
        structured qualitative clinical dimensions (concerns, stressors, symptoms).
        """
        tips = []
        concerns = [c.lower() for c in analysis_dict.get("presenting_concerns", [])]
        symptoms = [s.lower() for s in analysis_dict.get("symptoms_or_signals", [])]
        stressors = [st.lower() for st in analysis_dict.get("stressors", [])]

        combined = " ".join(concerns + symptoms + stressors)

        if "sleep" in combined or "insomnia" in combined:
            tips.append("**Sleep Restoration Strategy**: Practice a 30-minute cognitive wind-down before bed. Avoid screen exposure, and if awake for over 20 minutes, engage in quiet box breathing in a dim room.")
        
        if "academic" in combined or "university" in combined or "school" in combined:
            tips.append("**Academic Load Pacing**: Break study blocks into 25-minute Pomodoro segments with 5-minute cognitive breaks. Communicate with academic advisors or peer study circles to mitigate isolation.")

        if "social" in combined or "withdrawn" in combined or "alone" in combined:
            tips.append("**Gentle Social Reconnection**: Start with low-pressure contact — sending a simple text to one trusted friend or sitting in a shared communal space without pressure to perform.")

        if "energy" in combined or "fatigue" in combined or "exhaust" in combined:
            tips.append("**Energy Conservation**: Prioritize essential daily activities ('body no be firewood'). Allow yourself permission to rest and hydrate before attempting high-demand tasks.")

        if "financial" in combined or "money" in combined:
            tips.append("**Stress Compartmentalization**: Designate a specific 15-minute 'worry time' during daylight hours to outline immediate practical steps, preventing intrusive financial thoughts during rest periods.")

        # Default supportive guidance if no specific domain matched
        if not tips:
            tips = [
                "**Daily Emotional Check-in**: Acknowledge your emotional state without self-judgment. Emotional fluctuations are normal human responses to life challenges.",
                "**Engage Trusted Support**: Consider speaking openly with a counselor, close elder, or trusted confidant about what you are carrying.",
                "**Balanced Routine**: Maintain consistent meal times, adequate hydration, and brief daily outdoor walks to ground your physical rhythm."
            ]

        return {
            'title': "Evidence-Informed Supportive Guidance",
            'message': "Practical, qualitative coping strategies aligned with the presenting experiences:",
            'tips': tips
        }

    def format_recommendations(self, recommendations_dict):
        """
        Format recommendations for display
        """
        if not recommendations_dict:
            return ""
        
        formatted = f"### {recommendations_dict['title']}\n\n"
        formatted += f"{recommendations_dict['message']}\n\n"
        
        for i, tip in enumerate(recommendations_dict['tips'], 1):
            formatted += f"{i}. {tip}\n"
        
        return formatted