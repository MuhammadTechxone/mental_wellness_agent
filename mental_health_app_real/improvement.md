You are improving HeedX AI — a Nigerian mental wellness assistant designed around a controlled and explainable AI framework rather than a purely black-box generative system.

HeedX AI is currently under active development and research experimentation.
It is NOT a clinical diagnostic system.
It is a supportive wellness intelligence platform focused on:
- structured analysis
- controlled reasoning
- explainability
- cultural adaptation
- emotional safety
- low hallucination risk

==================================================
CURRENT ARCHITECTURE
==================================================

The current framework uses:
- TF-IDF vectorization
- Linear SVC classification
- sentence-level NLP analysis
- aggregated prediction logic
- session-based tracking
- Streamlit UI
- Groq-powered conversational support layer
- Nigerian wellness resources integration

The current workflow is approximately:

User Input
    ↓
Text Cleaning
    ↓
Sentence Splitting
    ↓
TF-IDF Vectorization
    ↓
Linear SVC Prediction
    ↓
Sentence-Level Classification
    ↓
Distribution Aggregation
    ↓
Risk Analysis
    ↓
Recommendations + Wellness Chat

==================================================
CORE FRAMEWORK PHILOSOPHY
==================================================

The architectural philosophy of HeedX AI is:

“Controlled intelligence over uncontrolled generation.”

The system intentionally prioritizes:
- explainability
- transparency
- modular reasoning
- predictable behavior
- interpretable outputs
- controlled NLP pipelines

instead of:
- opaque black-box outputs
- uncontrolled hallucinating systems
- emotionally unsafe autonomous reasoning

All improvements MUST preserve:
- safety
- explainability
- modularity
- controlled processing
- interpretability
- low hallucination risk

==================================================
YOUR TASK
==================================================

Improve the HeedX AI framework by introducing additional intelligent NLP reasoning layers WITHOUT destroying its controlled classical ML foundation.

The goal is to evolve HeedX AI into a:

- context-aware
- emotionally intelligent
- culturally adaptive
- safety-oriented
- explainable
mental wellness intelligence framework.

==================================================
REQUIRED IMPROVEMENTS
==================================================

# 1. SENTIMENT-AWARE PREPROCESSING LAYER

Introduce a preprocessing layer BEFORE SVC classification.

NEW LOGIC:

User Response
    ↓
Text Cleaning
    ↓
Sentiment Detection
    ↓
Emotion Weighting
    ↓
TF-IDF Vectorization
    ↓
SVC Classification

The system should:
- detect positive, negative, and neutral tone
- identify hopeful vs hopeless emotional structure
- improve handling of mixed-emotion statements

Example:
“I feel tired, but I still want to improve.”

The framework should detect:
- distress
- resilience
- recovery intent

instead of blindly leaning toward depression.

SUGGEST:
- VADER
- TextBlob
- custom emotional lexicons

==================================================
# 2. EMOTIONAL INTENSITY SCORING
==================================================

Add intensity-aware NLP logic.

Detect:
- mild emotional distress
- moderate distress
- severe emotional strain
- crisis-level urgency

Example:
- “I am stressed” → mild
- “I cannot handle this anymore” → severe

Use:
- adverbs
- repetition
- emotional keywords
- sentence emphasis
- urgency indicators

Intensity score should influence:
- risk calculation
- aggregation weighting
- escalation logic

==================================================
# 3. NEGATION-AWARE NLP
==================================================

Prevent dangerous false interpretation.

Examples:
- “I am not suicidal”
- “I no longer feel depressed”

The framework must understand:
- negation
- reversal
- emotional contradiction

Detect:
- not
- never
- no longer
- without
- cannot
- don't

Implement:
- negation tagging
- dependency parsing
- contextual token masking

Goal:
Reduce false crisis classification.

==================================================
# 4. CONTEXTUAL CONTINUITY ANALYSIS
==================================================

The current system analyzes many sentences independently.

Improve this by introducing:
- emotional flow tracking
- repeated pattern detection
- escalation trend analysis
- contradiction detection
- recovery trajectory analysis

Example sequence:
1. “I feel anxious.”
2. “I cannot sleep anymore.”
3. “Everything feels overwhelming.”

The framework should infer:
- escalating distress
- continuity of anxiety
- growing emotional burden

This becomes:
CONTEXTUAL AGGREGATION
instead of isolated sentence counting.

==================================================
# 5. ADVANCED AGGREGATION LOGIC
==================================================

Replace simplistic dominant-class counting.

NEW WEIGHTING FACTORS:
- prediction confidence
- emotional intensity
- repetition frequency
- contextual continuity
- crisis keyword presence
- sentiment polarity

Suggested architecture:

Sentence Prediction
    ↓
Confidence Weight
    ↓
Emotional Intensity Weight
    ↓
Contextual Continuity Weight
    ↓
Risk Aggregation Engine
    ↓
Final Wellness Assessment

Goal:
Produce more stable and psychologically sensible outcomes.

==================================================
# 6. HYBRID RULE-BASED SAFETY ENGINE
==================================================

Add a safety layer BEFORE ML prediction.

Purpose:
Ensure crisis language is NEVER ignored.

Detect:
- suicidal ideation
- self-harm indicators
- hopelessness
- emergency phrases
- existential despair

Example triggers:
- “I want to die”
- “Nobody would miss me”
- “I want everything to end”

The rule-based engine should:
- raise immediate risk score
- trigger emergency recommendations
- bypass uncertain ML ambiguity

This creates:
Hybrid Safety Intelligence

==================================================
# 7. EXPLAINABLE AI LAYER
==================================================

The framework must remain interpretable.

Add:
- keyword attribution
- emotional signal explanation
- confidence contribution breakdown
- detected distress markers
- dominant emotional indicators

Example output:

Prediction: Anxiety

Detected Signals:
- overthinking
- cannot sleep
- fear
- persistent worry

Confidence Contributors:
- repeated anxiety indicators
- negative sentiment intensity
- contextual continuity

Goal:
Allow researchers and reviewers to understand WHY predictions occur.

==================================================
# 8. NIGERIAN CONTEXTUAL LANGUAGE LAYER
==================================================

Improve local cultural adaptation.

Support:
- Nigerian English
- emotional slang
- pidgin expressions
- indirect distress language
- culturally contextual emotional communication

Examples:
- “My head is hot”
- “I am tired in my spirit”
- “Everything just weak me”

The system should interpret emotional meaning,
not literal wording only.

Goal:
Improve local emotional understanding.

==================================================
# 9. CONFIDENCE CALIBRATION
==================================================

Current SVC confidence estimation is limited.

Explore:
- CalibratedClassifierCV
- probability normalization
- weighted confidence fusion
- uncertainty estimation

Goal:
Avoid misleading certainty scores.

The framework should express:
- uncertainty
- ambiguity
- mixed emotional states

instead of fake precision.

==================================================
# 10. PRIVACY-FIRST ARCHITECTURE
==================================================

Preserve:
- session-based storage
- local interpretability
- minimal cloud dependency
- browser-session privacy

Avoid:
- unnecessary permanent storage
- invasive profiling
- hidden behavioral tracking

==================================================
# 11. FUTURE RESEARCH DIRECTIONS
==================================================

Suggest future directions such as:
- Hausa NLP support
- multilingual African wellness datasets
- Ajami-assisted emotional analysis
- transformer-assisted explanation layers
- conversational emotional memory
- adaptive coping recommendation systems
- federated privacy-preserving wellness AI

==================================================
EXPECTED RESPONSE STYLE
==================================================

When proposing improvements:
- explain WHY the improvement matters
- explain HOW it works technically
- explain HOW it improves safety
- preserve modular architecture
- preserve explainability
- avoid overengineering
- remain realistic for:
    - Python
    - Streamlit
    - scikit-learn
    - NLP utility pipelines

==================================================
IMPORTANT RESTRICTIONS
==================================================

DO NOT:
- turn the system into an autonomous therapist
- claim diagnostic authority
- replace controlled reasoning with uncontrolled generation
- remove explainability
- sacrifice safety for sophistication

This framework is intentionally:
- controlled
- interpretable
- modular
- safety-aware
- research-oriented
- development-stage

The objective is to build:
A safer and more explainable wellness intelligence framework for Nigerian and African contexts.