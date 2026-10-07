"""
Centralized Lexicons for HeedX AI
Contains keywords for Rule-Based Safety, Intensity, Resilience, and Cultural Idioms.
"""

# Nigerian Contextual Idiom Mapping
# Maps local expressions to standard emotional equivalents
NIGERIAN_IDIOM_MAP = {
    "head is hot": "stressed and overwhelmed",
    "weak my spirit": "depressed and discouraged",
    "body is doing me": "feeling unwell or anxious",
    "body no be firewood": "physically and mentally exhausted",
    "heart is cutting": "anxious or fearful",
    "no joy": "depressed and empty",
    "mind is heavy": "sad and worried",
    "mind fly": "panic attack or dissociation",
    "chest tight": "anxiety or panic symptoms",
    "no get power": "fatigued and low energy",
    "life is hard": "struggling",
    "not easy": "difficult",
    "not okay": "distressed",
    "not ok": "distressed",
    "not fine": "unwell",
    "no be small": "extremely severe",
    "inside life": "facing complex existential problems",
    "carry matter for head": "overthinking or obsessive worry",
    "spirit is low": "depressed",
    "everything just weak me": "overwhelmed and helpless",
    "i don taya": "i am exhausted and giving up",
    "thank god": "grateful and normal",
    "god help me": "distressed and seeking help",
    "no vibe": "loss of interest",
    "i want to kpai": "suicidal intent",
    "i dey try": "i am trying and resilient",
    "belle no sweet": "unhappy or dissatisfied",
    "taya": "exhausted",
    "life tire me": "suicidal ideation",
    "eye clear": "facing harsh reality or stress",
    "vibe finish": "loss of interest or anhedonia",
    "no hope": "hopeless and despairing",
    "world people": "external stressors or social anxiety",
    "pressure": "intense stress",
    "tension": "anxiety"
}

# Intensity Modifiers
INTENSITY_KEYWORDS = {
    'high': [
        'very', 'extremely', 'really', 'too', 'cannot', 'cant', 'never', 'always',
        'worst', 'terrible', 'completely', 'totally', 'absolutely', 'severely',
        'unbearably', 'excessively', 'deeply', 'highly', 'utterly', 'drastically',
        'uncontrollably', 'violently', 'desperately', 'massively', 'horribly'
    ],
    'moderate': [
        'quite', 'fairly', 'somewhat', 'bit', 'slightly', 'rather', 'mostly',
        'relatively', 'mildly', 'partially', 'kind of', 'sort of', 'moderately'
    ]
}

# Resilience and Hope Indicators
RESILIENCE_KEYWORDS = [
    'trying', 'hoping', 'better', 'improve', 'work on', 'pray', 'support',
    'help', 'therapy', 'recovery', 'strong', 'survive', 'healing', 'growth',
    'overcoming', 'moving on', 'faith', 'patience', 'endure', 'strength',
    'optimistic', 'counselling', 'meditation', 'exercise', 'persistence',
    'steady', 'rising', 'community', 'ubuntu', 'hopeful', 'striving'
]

# Crisis and Self-Harm Triggers (Regex compatible)
CRISIS_TRIGGERS = [
    r"want to die", r"kill\s*my\s*self", r"kill\s*myself", r"end it all",
    r"no reason to live", r"take\s*my\s*life", r"hurt\s*my\s*self",
    r"hurt\s*myself", r"better off dead", r"suicide", r"end my life",
    r"don't want to be here", r"no point in living", r"painless death",
    r"goodbye world", r"everyone better off without me", r"buy sniper",
    r"drink otapiapia", r"hang\s*my\s*self", r"don't want to wake up",
    r"want to sleep forever", r"bye for real"
]

# Negation words to detect reversals
NEGATIONS = [
    'not', 'no', 'never', 'dont', 'doesnt', 'wasnt', 'neither', 'nor', 
    'cant', 'cannot', 'isnt', 'arent', 'werent', 'havent', 'hasnt', 'didnt'
]

# Indicators of normal/positive mental state
WELLNESS_KEYWORDS = [
    'okay', 'ok', 'ky', 'fine', 'good', 'well', 'alright', 'cool', 'happy', 
    'blessed', 'peace', 'joy', 'stable', 'calm', 'rested', 'satisfied'
]