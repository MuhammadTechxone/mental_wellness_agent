---
title: HeedX AI
emoji: 🇳🇬
colorFrom: green
colorTo: gray
sdk: streamlit
sdk_version: 1.31.0
app_file: mental_app.py
pinned: false
---

# 🇳🇬 HeedX AI — Nigerian Mental Wellness & Clinical Decision Support

## Overview

HeedX AI is a two-mode mental health intelligence platform designed specifically for Nigerian contexts. It provides:

1. Mode A: Professional Case Analysis
   - For psychologists, psychiatrists, researchers, and case officers
   - Upload patient observations and receive structured qualitative analysis and evidence-grounded insights

2. Mode B: Conversational User Support
   - For individuals seeking empathetic, culturally sensitive mental wellness dialogue
   - Provides multi-turn support with context-aware, evidence-informed responses

Both modes share a unified architecture built on qualitative semantic understanding, retrieval-augmented generation (RAG), and dedicated safety protocols — not diagnostic percentages.

## Key Features

### Professional Mode (Case Analysis)
- Upload or paste patient/client observations (.pdf, .txt, or direct text)
- Structured qualitative extraction of:
  - Presenting concerns
  - Symptoms and signals
  - Duration and trajectory
  - Stressors and sociocultural context
  - Functional impact
  - Risk indicators and safety signals
  - Protective factors and resilience
- Evidence-grounded case formulation using Nigerian clinical literature and research
- Downloadable structured summaries for professional review
- Explicit safety triage separate from standard analysis

### Conversational Mode (User Chat)
- Natural multi-turn dialogue
- Automatic conversation state tracking
- Context-aware, evidence-informed responses
- Dedicated crisis detection and immediate safety escalation
- No diagnostic claims — supportive understanding only
- Warm, culturally attuned Nigerian mental wellness tone

### Shared Core Components
- Qualitative Analysis Engine
- RAG System
- Safety Layer
- Conversation State Manager
- Deterministic Support Modules

## No Diagnostic Percentages

Unlike traditional mental health AI, HeedX does not:
- Generate synthetic diagnostic percentages
- Claim clinical diagnoses
- Use a four-class ML classifier as the main inference engine
- Force complex human experience into artificial categories

Instead, HeedX provides qualitative clinical understanding grounded in evidence and cultural context.

## Nigerian Context
- Crisis hotlines (MANI, She Writes Woman, National Emergency)
- Federal Neuropsychiatric Hospital directories
- Faith and community support networks
- Nigerian proverbs and cultural wisdom
- Support for Nigerian English and idiomatic expressions
- Evidence from Nigerian epidemiological research

## Quick Start

```bash
cd mental_health_app_real
pip install -r requirements.txt
streamlit run mental_app.py
