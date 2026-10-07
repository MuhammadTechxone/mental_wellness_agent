# HeedX AI — Two-Mode Mental-Health AI Architecture

You are the primary AI software engineer working on **HeedX AI**, a Nigerian mental-health support and analysis application.

Your first responsibility is to **understand the existing codebase and architecture before changing it**.

Do not immediately rewrite the application.

Inspect the existing project, identify what is already working, and then redesign it around the architecture described below.

---

# 1. CORE CONCEPT

HeedX has **TWO DISTINCT INPUT MODES**.

They must remain conceptually separate even though they can share the same underlying AI/RAG infrastructure.

## Mode A — Professional / Case Analysis

This mode is intended for a psychologist, mental-health professional, researcher, or authorized user who already has patient/client text.

The professional can:

* upload a document
* paste patient/client text
* write patient/client text manually

HeedX then performs **qualitative analysis** of the supplied text.

Example:

> "The patient reports feeling persistently sad for approximately one month. She has difficulty sleeping, has withdrawn from friends, and is struggling to concentrate at university."

The system extracts and organizes information such as:

```text
Presenting concerns
• persistent sadness
• sleep difficulty
• social withdrawal
• difficulty concentrating

Duration
• approximately one month

Context
• university/academic environment

Potentially relevant symptoms/signals
• low mood
• sleep disturbance
• reduced social engagement
• concentration difficulty

Risk information
• no suicidal ideation established from the supplied text
• further assessment may be appropriate
```

This is **qualitative analysis**.

Do NOT turn this into:

```text
Depression = 78%
Anxiety = 15%
Normal = 5%
Suicidal = 2%
```

The system should not generate fake diagnostic probabilities.

---

# 2. Mode B — Conversational User Mode

This mode is for a person directly interacting with HeedX.

The user communicates naturally:

> "I've been feeling really down lately."

Then:

> "It's been happening for a few weeks and I can't sleep properly."

Then:

> "University has also been stressful."

The system should maintain conversation context and continuously update its understanding.

Conceptually:

```text
USER MESSAGE
      ↓
UNDERSTAND CURRENT MESSAGE
      ↓
UPDATE CONVERSATION STATE
      ↓
RETRIEVE RELEVANT KNOWLEDGE
      ↓
LLM
      ↓
PERSONALIZED RESPONSE
      ↓
USER CONTINUES
      ↓
REPEAT
```

This mode should feel like a natural conversation, NOT like filling out a questionnaire.

---

# 3. VERY IMPORTANT: DO NOT ADD QUESTIONNAIRE SCREENING

For the current version, do NOT implement:

* PHQ-9
* GAD-7
* WHO-5
* Kessler
* questionnaire scoring
* questionnaire UI
* questionnaire-based diagnosis

This may be added in a future version.

The current system should primarily understand natural language.

---

# 4. VERY IMPORTANT: OLD CLASSIFIER IS NO LONGER THE PRIMARY ENGINE

The existing application may contain a classical ML classifier with classes such as:

```text
Normal
Anxiety
Depression
Suicidal
```

The old architecture was approximately:

```text
INPUT
  ↓
CLASSICAL ML MODEL
  ↓
class + probabilities
  ↓
Python analysis
  ↓
LLM
  ↓
conversation
```

This classifier should NOT be the primary inference mechanism in the redesigned system.

It may be retained for:

* experimentation
* research comparison
* benchmarking
* future development

But the production user experience should NOT depend on the four-class classifier.

The new architecture is based on **qualitative semantic understanding + retrieval + conversational generation**.

---

# 5. TWO INPUTS, ONE SHARED INTELLIGENCE LAYER

The central architectural principle is:

```text
                    HEEDX
                      │
            ┌─────────┴─────────┐
            │                   │
            ▼                   ▼
    PROFESSIONAL MODE      CONVERSATION MODE
     CASE ANALYSIS            USER CHAT
            │                   │
            ▼                   ▼
    Qualitative analysis    Conversation
            │               understanding
            │                   │
            └─────────┬─────────┘
                      ▼
              SHARED HEEDX CORE
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
    Analysis        RAG          Safety
     Engine        Engine         Layer
        │             │             │
        └─────────────┼─────────────┘
                      ▼
                     LLM
                      │
             ┌────────┴────────┐
             ▼                 ▼
       Case output        User response
```

Do NOT build two completely unrelated AI systems.

Build two input experiences that share common underlying services.

---

# 6. WHAT "QUALITATIVE ANALYSIS" MEANS

The analysis engine should identify meaningful information from text rather than forcing it into mutually exclusive diagnostic categories.

Potential structured fields include:

```json
{
  "presenting_concerns": [],
  "emotions": [],
  "symptoms_or_signals": [],
  "stressors": [],
  "duration": null,
  "functional_impact": [],
  "social_context": [],
  "protective_factors": [],
  "risk_signals": [],
  "support_needs": [],
  "uncertainties": []
}
```

This is an **information representation**, not a diagnosis.

For example:

```json
{
  "presenting_concerns": [
    "persistent sadness"
  ],
  "symptoms_or_signals": [
    "sleep difficulty",
    "loss of interest",
    "social withdrawal"
  ],
  "stressors": [
    "academic pressure"
  ],
  "duration": "approximately three weeks",
  "risk_signals": [],
  "uncertainties": [
    "suicidal ideation not established"
  ]
}
```

The system should distinguish between:

* explicitly stated information
* reasonable semantic interpretation
* information that remains unknown

Do not invent information that the user/patient did not provide.

---

# 7. PROFESSIONAL / CASE ANALYSIS PIPELINE

The professional mode should follow:

```text
PROFESSIONAL
     │
     ▼
Upload / Paste / Write Patient Text
     │
     ▼
Text Extraction
     │
     ▼
Qualitative Analysis
     │
     ├── concerns
     ├── symptoms/signals
     ├── emotions
     ├── stressors
     ├── duration
     ├── functioning
     ├── context
     └── risk signals
     │
     ▼
Structured Case Representation
     │
     ▼
Retrieval Query Construction
     │
     ▼
Embedding
     │
     ▼
Vector Search
     │
     ▼
Relevant Evidence
     │
     ▼
LLM
     │
     ▼
Professional Case Summary / Evidence-Grounded Analysis
```

The professional should be able to see the resulting analysis clearly.

---

# 8. CONVERSATIONAL PIPELINE

The conversational mode should follow:

```text
USER
  │
  ▼
Message
  │
  ▼
Conversation Understanding
  │
  ├── current concerns
  ├── symptoms/signals
  ├── emotions
  ├── stressors
  ├── duration
  └── risk signals
  │
  ▼
Update Conversation State
  │
  ▼
Construct Retrieval Query
  │
  ▼
Embedding
  │
  ▼
Vector Search
  │
  ▼
Relevant Evidence
  │
  ▼
LLM
  │
  ▼
Natural Personalized Response
  │
  ▼
USER
```

This process can repeat on every meaningful turn.

---

# 9. CONVERSATION STATE

The conversational system should maintain a structured state.

Example:

```json
{
  "main_concerns": [
    "persistent sadness",
    "sleep difficulty",
    "loss of interest"
  ],
  "duration": "approximately three weeks",
  "stressors": [
    "academic pressure",
    "financial difficulty"
  ],
  "functional_impact": [
    "difficulty concentrating"
  ],
  "risk_signals": [],
  "risk_status": "not_established"
}
```

The state must evolve as the user provides new information.

For example:

### First message

> "I've been feeling down."

State:

```text
low mood
```

### Second message

> "For about three weeks and I can't sleep."

State becomes:

```text
low mood
+
three-week duration
+
sleep difficulty
```

### Third message

> "University has been stressful."

State becomes:

```text
low mood
+
three-week duration
+
sleep difficulty
+
academic stress
```

This state should help improve retrieval and personalization.

---

# 10. EMBEDDINGS AND VECTORS

There are TWO sides to embeddings.

## Static knowledge embeddings

Knowledge documents are processed before user interaction:

```text
Research / Guidelines / Knowledge
          ↓
      Text extraction
          ↓
        Chunking
          ↓
     Embedding model
          ↓
        Vectors
          ↓
     Vector database
```

These embeddings are relatively static.

## User/query embeddings

When relevant user information needs to be retrieved:

```text
Current user message
        +
Conversation state
        +
Structured signals
        ↓
Retrieval query
        ↓
Embedding model
        ↓
Query vector
        ↓
Vector similarity search
```

The same compatible embedding model should be used for knowledge chunks and retrieval queries.

Remember:

> The vector does not contain the knowledge itself.

The actual knowledge remains in the stored document chunks.

The vector allows the system to find semantically related chunks.

---

# 11. RETRIEVAL MUST USE THE USER'S INFORMATION

Do not build a RAG system where the user text is disconnected from retrieval.

The connection should be explicit:

```text
USER TEXT
   ↓
UNDERSTANDING
   ↓
STRUCTURED SIGNALS
   ↓
RETRIEVAL QUERY
   ↓
EMBEDDING
   ↓
VECTOR SEARCH
   ↓
RELEVANT KNOWLEDGE
```

For example:

User:

> "I haven't enjoyed football for weeks and I'm barely sleeping."

Possible retrieval representation:

```text
loss of interest
sleep disturbance
persistent symptoms
reduced enjoyment
mental health
```

The system then searches the knowledge base for semantically relevant evidence.

---

# 12. DO NOT BLINDLY EMBED THE ENTIRE CONVERSATION

The system should not simply concatenate every historical message forever and embed everything blindly.

Instead use:

```text
Current message
+
Relevant conversation state
+
Relevant context
+
Structured signals
```

to construct the retrieval query.

The full conversation history can still be supplied to the LLM where appropriate.

Retrieval context and conversational context are related but are not identical.

---

# 13. RAG KNOWLEDGE BASE

The knowledge base should be designed around reliable mental-health information, especially Nigerian/local context.

Suggested structure:

```text
knowledge/
│
├── nigeria_evidence/
│   ├── national/
│   ├── depression/
│   ├── anxiety/
│   ├── suicide/
│   ├── trauma/
│   ├── substance_use/
│   ├── adolescents/
│   ├── university_students/
│   └── severe_mental_illness/
│
├── nigeria_context/
│   ├── stigma/
│   ├── culture/
│   ├── family/
│   ├── religion_and_mental_health/
│   ├── unemployment/
│   ├── poverty/
│   ├── conflict/
│   └── healthcare_access/
│
├── scenarios/
│   ├── academic_stress/
│   ├── financial_stress/
│   ├── grief/
│   ├── relationships/
│   ├── anxiety/
│   ├── depression/
│   ├── trauma/
│   └── suicide_risk/
│
├── psychoeducation/
│
├── recommendations/
│
└── metadata/
```

Do not simply dump documents into a vector database.

Preserve useful metadata.

---

# 14. KNOWLEDGE CHUNK METADATA

Where possible, each chunk should retain:

```text
document_id
title
source
authors
year
country
state
population
sample_size
age_range
mental_health_domain
condition
study_design
measurement_tool
evidence_level
limitations
source_url
```

This allows future retrieval filtering and source attribution.

---

# 15. DETERMINISTIC MODULES STILL EXIST

RAG does NOT replace every existing static module.

Keep exact information in deterministic/structured data.

Examples:

```text
Emergency contacts
Facilities
Facility addresses
Verified URLs
Crisis procedures
Service directories
Application configuration
Other exact structured information
```

Do not ask the LLM to invent these.

The architecture should therefore have:

```text
                  HEEDX CORE
                     │
        ┌────────────┼─────────────┐
        │            │             │
        ▼            ▼             ▼
      LLM           RAG        DETERMINISTIC
 Conversation     Knowledge       Modules
        │            │             │
        │            │             ├── contacts
        │            │             ├── facilities
        │            │             ├── URLs
        │            │             └── exact data
        │            │
        │            ├── studies
        │            ├── guidance
        │            ├── psychoeducation
        │            └── evidence
        │
        └────────────┬─────────────┘
                     ▼
                  HEEDX
```

---

# 16. SAFETY LAYER

Safety must be separate from ordinary RAG.

For example, if a user says:

> "I want to kill myself."

the application must not simply perform normal semantic retrieval and answer like an ordinary mental-health question.

It must activate a dedicated safety pathway.

The safety layer should be able to:

* identify high-risk signals
* determine whether clarification is necessary
* prioritize immediate safety
* provide verified emergency/crisis resources
* encourage appropriate human support
* change the response strategy
* prevent unsafe conversational behavior

RAG can provide supporting evidence, but the safety mechanism itself must have explicit rules and guardrails.

---

# 17. NO DIAGNOSTIC CLAIMS

HeedX should not claim:

> "You have depression."

based solely on conversational analysis.

Prefer:

> "What you're describing includes experiences commonly associated with depression."

or:

> "These symptoms may be worth discussing with a mental-health professional."

The system is providing **support, qualitative analysis, and evidence-grounded information**, not replacing clinical diagnosis.

---

# 18. PROFESSIONAL OUTPUT VS USER OUTPUT

These two modes should have different presentation styles.

## Professional mode

The output can be structured:

```text
CASE ANALYSIS

Presenting concerns
...

Reported symptoms/signals
...

Duration
...

Stressors/context
...

Functional impact
...

Risk indicators
...

Relevant considerations
...

Evidence retrieved
...

Suggested areas for further assessment
...
```

Be clear that this is an AI-assisted analysis and not a definitive diagnosis.

## Conversational mode

The output should be natural:

```text
"I hear you. From what you've described, you've been dealing
with poor sleep and losing interest in things you normally enjoy.
That can be difficult, especially alongside academic stress.

Can I ask whether this has also affected your ability to attend
classes or carry out your normal daily activities?"
```

Do not expose vector databases, embeddings, retrieval mechanics, or internal analysis unless specifically requested.

---

# 19. LLM CONTEXT

The LLM should receive an appropriate combination of:

```text
System instructions
+
Current user/patient text
+
Relevant conversation history
+
Structured analysis
+
Conversation/case state
+
Retrieved evidence
+
Safety state
+
Deterministic information when required
```

For professional mode:

```text
Patient text
+
Qualitative analysis
+
Retrieved evidence
+
Safety information
+
Professional instructions
```

For conversational mode:

```text
Current user message
+
Conversation history
+
Conversation state
+
Retrieved evidence
+
Safety state
+
Conversational instructions
```

---

# 20. KNOWLEDGE SOURCES

The knowledge system should prioritize reliable sources such as:

* peer-reviewed Nigerian research
* reputable international research
* WHO guidance
* Nigerian government/public-health sources
* recognized clinical/public-health organizations
* evidence-based mental-health resources

Nigerian evidence should be prioritized where relevant.

Do not fabricate citations or sources.

---

# 21. EXISTING CODEBASE INSPECTION

Before changing the project, inspect:

1. Entry point
2. UI
3. Professional/case-analysis interface
4. Conversational interface
5. Existing classical ML model
6. Existing Python analysis
7. Existing LLM integration
8. Existing static modules
9. Existing recommendations
10. Emergency/crisis information
11. Facility/location data
12. Data files
13. Deployment configuration
14. Requirements/dependencies
15. Existing tests

Determine what should be:

* preserved
* refactored
* replaced
* deprecated
* newly added

Do not delete existing functionality simply because the architecture is changing.

---

# 22. TARGET ARCHITECTURE

The final conceptual architecture should resemble:

```text
                         HEEDX AI
                            │
             ┌──────────────┴──────────────┐
             │                             │
             ▼                             ▼
     PROFESSIONAL MODE              CONVERSATIONAL MODE
       CASE ANALYSIS                    USER CHAT
             │                             │
     Upload / Paste / Write           User messages
             │                             │
             ▼                             ▼
      Qualitative Analysis          Conversation Understanding
             │                             │
             ▼                             ▼
      Structured Case State         Conversation State
             │                             │
             └──────────────┬──────────────┘
                            ▼
                   RETRIEVAL ENGINE
                            │
                      Query creation
                            ↓
                       Embedding
                            ↓
                    Vector Database
                            ↓
                   Relevant Knowledge
                            │
             ┌──────────────┼──────────────┐
             │              │              │
             ▼              ▼              ▼
            RAG          SAFETY       DETERMINISTIC
         Evidence         Layer          Modules
             │              │              │
             └──────────────┼──────────────┘
                            ▼
                           LLM
                     ┌──────┴──────┐
                     ▼             ▼
             Professional       User-facing
                output           response
```

---

# 23. DEVELOPMENT ORDER

Implement incrementally.

### Stage 1 — Repository analysis

Understand the existing application.

Do not make destructive changes.

### Stage 2 — Separate the two input modes

Ensure the UI and backend conceptually distinguish:

```text
Professional / Case Analysis
```

from:

```text
Conversational User Mode
```

### Stage 3 — Build/refactor qualitative analysis

Create a structured qualitative analysis representation.

### Stage 4 — Build knowledge ingestion

Implement:

```text
documents
→ extraction
→ chunking
→ metadata
→ embeddings
→ vector storage
```

### Stage 5 — Implement retrieval

Implement:

```text
query
→ embedding
→ similarity search
→ relevant chunks
```

### Stage 6 — Connect retrieval to professional analysis

```text
patient text
→ qualitative analysis
→ retrieval
→ evidence
→ professional output
```

### Stage 7 — Connect retrieval to conversation

```text
user message
→ conversation understanding
→ state
→ retrieval
→ evidence
→ LLM
→ response
```

### Stage 8 — Implement safety layer

Keep safety behavior separate from ordinary RAG.

### Stage 9 — Test both modes separately

Test professional analysis independently from conversational behavior.

### Stage 10 — Integrate and refine UI

Only after the underlying architecture is working.

---

# 24. TEST CASES

Create tests/examples for both modes.

## Professional mode example

Input:

> "Patient reports feeling sad most days for the past month, has stopped enjoying social activities and is having difficulty sleeping. Academic workload has increased significantly."

Expected qualitative analysis should identify:

```text
persistent sadness
reduced interest/social withdrawal
sleep difficulty
academic stress
approximately one month duration
```

It should NOT output a fabricated diagnostic probability.

## Conversational mode example

User:

> "I've been feeling down lately."

Then:

> "It's been about three weeks and I barely sleep."

Then:

> "School has also been stressful."

The system should progressively update the conversation state and retrieve increasingly relevant evidence.

---

# 25. FINAL DESIGN PRINCIPLE

The most important architecture to preserve is:

```text
                 TWO INPUT MODES
                       │
          ┌────────────┴────────────┐
          │                         │
          ▼                         ▼
   PROFESSIONAL MODE          CONVERSATION MODE
          │                         │
   Qualitative analysis       Continuous understanding
          │                         │
          └────────────┬────────────┘
                       ▼
                 SHARED CORE
                       │
             ┌─────────┼─────────┐
             ▼         ▼         ▼
          Analysis    RAG      Safety
                       │
                  Embeddings
                       │
                  Vector search
                       │
                       ▼
                      LLM
                       │
             ┌─────────┴─────────┐
             ▼                   ▼
      Professional output   User response
```

Remember these principles throughout implementation:

1. **There are two distinct input modes.**
2. **Professional mode analyzes supplied patient/client text.**
3. **Conversational mode interacts continuously with the user.**
4. **The analysis is primarily qualitative, not a four-class probability prediction.**
5. **No questionnaire screening in this version.**
6. **RAG is shared infrastructure for both modes.**
7. **Knowledge documents are embedded and stored as vectors.**
8. **User/conversation information produces query embeddings for retrieval.**
9. **The user's actual text remains central; embeddings only facilitate retrieval.**
10. **Conversation state is maintained separately from the vector database.**
11. **Deterministic modules remain responsible for exact information.**
12. **Safety has its own explicit layer.**
13. **RAG provides evidence; it does not diagnose.**
14. **The LLM turns the analysis, context, evidence, and safety state into the appropriate output.**

Before implementing major changes, first inspect the repository and produce:

1. **Current architecture**
2. **Target architecture**
3. **Files/components that should be preserved**
4. **Files/components that should be changed**
5. **New components required**
6. **Implementation sequence**

Then proceed incrementally without unnecessarily destroying existing working functionality.
