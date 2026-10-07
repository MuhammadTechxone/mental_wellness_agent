"""
HeedX AI — Nigerian Mental Wellness Platform
Two-Mode Mental-Health AI Architecture:
- Mode A: Professional / Case Analysis (Qualitative Case Understanding + RAG + Clinical Formulation)
- Mode B: Conversational User Mode (Multi-turn State Tracking + RAG + Safety-First Dialogue)
- Nigerian Resources Directory: Verified emergency, psychiatric, and community support
"""

# ============================================
# IMPORTS
# ============================================
import html as html_lib
import os
import random
import urllib.parse
from datetime import datetime
from typing import Dict, List, Any, Optional

import numpy as np
import pandas as pd
import pypdf
import requests
import streamlit as st

try:
    import google.generativeai as genai
except ImportError:
    genai = None

from config.settings import (
    CONTACT_INFO,
    NIGERIA_EMERGENCY_NUMBERS, MENTAL_HEALTH_SUPPORT,
    PROFESSIONAL_HELP, FAITH_COMMUNITY_SUPPORT,
    NIGERIAN_PROVERBS, CULTURAL_WELLNESS_TIPS, CRISIS_RESOURCES
)
from utils.recommendations import RecommendationEngine
from utils.session_storage import SessionTracker
from utils.qualitative_engine import QualitativeAnalysisEngine
from utils.rag_engine import RAGEngine
from utils.safety_layer import SafetyLayer
from utils.conversation_state import ConversationStateManager

# ============================================
# PAGE CONFIGURATION
# ============================================
st.set_page_config(
    page_title="HeedX AI — Nigerian Mental Wellness",
    page_icon="🇳🇬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CUSTOM CSS — Professional, Accessible, Cultural
# ============================================
st.markdown("""
<style>
    /* Typography & base */
    html, body, [class*="css"] {
        font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
    }
    .main-header {
        font-size: 2.1rem;
        font-weight: 700;
        color: #0f2e1e;
        text-align: center;
        letter-spacing: -0.5px;
        margin-bottom: 0.2rem;
    }
    .main-subtitle {
        text-align: center;
        color: #008751;
        font-size: 1.05rem;
        font-weight: 600;
        margin-bottom: 0.2rem;
    }
    .main-tagline {
        text-align: center;
        color: #4a5568;
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.35rem;
        font-weight: 600;
        color: #1a202c;
        margin-bottom: 0.75rem;
    }
    .nigeria-accent {
        height: 4px;
        background: linear-gradient(90deg, #008751 33%, #ffffff 33%, #ffffff 66%, #008751 66%);
        border-radius: 2px;
        margin: 0.5rem auto 1.2rem auto;
        max-width: 320px;
    }

    /* Cards */
    .feature-card {
        background-color: #ffffff;
        border-radius: 0.6rem;
        padding: 1.2rem;
        margin-bottom: 0.8rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
        transition: transform 0.2s ease;
    }
    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    .clinical-card {
        background-color: #f7fafc;
        border-left: 4px solid #008751;
        padding: 0.9rem 1.1rem;
        border-radius: 0.35rem;
        margin: 0.5rem 0;
        color: #2d3748;
    }
    .evidence-card {
        background-color: #f0fdf4;
        border-left: 4px solid #16a34a;
        padding: 0.9rem 1.1rem;
        border-radius: 0.35rem;
        margin: 0.5rem 0;
        font-size: 0.92rem;
    }
    .safety-alert-card {
        background-color: #fef2f2;
        border-left: 5px solid #dc2626;
        padding: 1.2rem;
        border-radius: 0.5rem;
        margin: 0.8rem 0;
        color: #991b1b;
    }

    /* Buttons */
    .stButton > button {
        width: 100%;
        background-color: #008751;
        color: white;
        font-weight: 600;
        border-radius: 0.4rem;
        border: none;
        padding: 0.5rem 1rem;
        transition: all 0.25s ease;
    }
    .stButton > button:hover {
        background-color: #006640;
        color: white;
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.12);
    }

    /* Contact Links */
    .contact-button {
        display: block;
        text-align: center;
        padding: 0.45rem 1rem;
        margin: 0.25rem 0;
        border-radius: 0.35rem;
        text-decoration: none;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .contact-whatsapp {
        background-color: #25D366;
        color: white !important;
    }
    .contact-email {
        background-color: #4a5568;
        color: white !important;
    }

    /* Chat bubble styling */
    .chat-user {
        background-color: #e6f4ea;
        color: #1a202c;
        padding: 0.8rem 1rem;
        border-radius: 0.75rem 0.75rem 0.1rem 0.75rem;
        margin: 0.4rem 0;
        max-width: 85%;
        margin-left: auto;
    }
    .chat-assistant {
        background-color: #ffffff;
        color: #1a202c;
        border: 1px solid #e2e8f0;
        padding: 0.9rem 1.1rem;
        border-radius: 0.75rem 0.75rem 0.75rem 0.1rem;
        margin: 0.4rem 0;
        max-width: 88%;
        box-shadow: 0 1px 4px rgba(0,0,0,0.03);
    }

    /* Disclaimer */
    .disclaimer {
        font-size: 0.82rem;
        color: #718096;
        font-style: italic;
        margin-top: 2rem;
        padding: 1rem;
        border-top: 1px solid #e2e8f0;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# SHARED CORE SINGLETONS & SESSION STATE
# ============================================
@st.cache_resource
def get_shared_core():
    """Initializes and caches the shared HeedX core engines"""
    qualitative_engine = QualitativeAnalysisEngine()
    rag_engine = RAGEngine()
    safety_layer = SafetyLayer()
    recommendation_engine = RecommendationEngine()
    return qualitative_engine, rag_engine, safety_layer, recommendation_engine


def init_session_state():
    """Initializes session variables with clean state defaults"""
    defaults = {
        'page': 'home',  # 'home', 'mode_a', 'mode_b', 'resources'
        'gemini_api_key': '',
        'case_text': '',
        'case_analysis': None,
        'case_evidence': [],
        'case_formulation': '',
        'conversation_manager': ConversationStateManager(),
        'chat_messages': [],
        'active_crisis_banner': None,
        'tracker': SessionTracker(),
        'uploader_id': 0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

    # Resolve API Key
    if not st.session_state.gemini_api_key:
        try:
            st.session_state.gemini_api_key = st.secrets.get("GEMINI_API_KEY", "")
        except Exception:
            pass
    if not st.session_state.gemini_api_key:
        st.session_state.gemini_api_key = os.environ.get("GEMINI_API_KEY", "")


# ============================================
# LLM SERVICE (GEMINI WITH ROBUST FALLBACK)
# ============================================
GEMINI_MODEL = "gemini-1.5-flash"

def call_gemini_service(
    messages: List[Dict[str, str]],
    api_key: str,
    system_instruction: Optional[str] = None,
    temperature: float = 0.5,
    max_tokens: int = 1000
) -> str:
    """
    Calls Google Gemini via SDK or direct REST with error handling.
    """
    if not api_key or not str(api_key).strip():
        return (
            "Gemini API key is not configured. "
            "Please provide a Gemini API key in the sidebar or in `.streamlit/secrets.toml`."
        )

    api_key = str(api_key).strip()

    # Strategy 1: google.generativeai SDK
    if genai is not None:
        try:
            genai.configure(api_key=api_key)
            model_kwargs = {"model_name": GEMINI_MODEL}
            if system_instruction:
                model_kwargs["system_instruction"] = system_instruction
            if hasattr(genai, "types") and hasattr(genai.types, "GenerationConfig"):
                model_kwargs["generation_config"] = genai.types.GenerationConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens
                )
            model = genai.GenerativeModel(**model_kwargs)

            chat_history = []
            current_prompt = "Hello"
            for m in messages:
                role = m.get("role", "")
                content = m.get("content", "")
                if role in ["user", "human"]:
                    chat_history.append({"role": "user", "parts": [content]})
                elif role in ["assistant", "model", "bot"]:
                    chat_history.append({"role": "model", "parts": [content]})

            if chat_history and chat_history[-1]["role"] == "user":
                current_prompt = chat_history.pop()["parts"][0]

            chat = model.start_chat(history=chat_history)
            response = chat.send_message(current_prompt)
            if response and response.text:
                return response.text.strip()
        except Exception:
            pass  # Fallback to direct REST

    # Strategy 2: Direct REST endpoint (zero dependency, highly reliable)
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={api_key}"
        headers = {"Content-Type": "application/json"}

        contents_payload = []
        for m in messages:
            role = "user" if m.get("role") in ["user", "human"] else "model"
            contents_payload.append({
                "role": role,
                "parts": [{"text": m.get("content", "")}]
            })

        body = {
            "contents": contents_payload,
            "generationConfig": {
                "temperature": temperature,
                "maxOutputTokens": max_tokens
            }
        }
        if system_instruction:
            body["system_instruction"] = {
                "parts": [{"text": system_instruction}]
            }

        resp = requests.post(url, headers=headers, json=body, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            candidates = data.get("candidates", [])
            if candidates:
                cand = candidates[0]
                parts = cand.get("content", {}).get("parts", [])
                if parts and "text" in parts[0]:
                    return parts[0]["text"].strip()
            return "No response text generated from the service."
        else:
            return f"Gemini API returned status {resp.status_code}: {resp.text[:180]}"
    except Exception as err:
        return f"Service connection error: {err}"


# ============================================
# SIDEBAR NAVIGATION & CONTACTS
# ============================================
def render_sidebar():
    """Renders the persistent application sidebar"""
    with st.sidebar:
        st.markdown(
            "<div style='text-align:center;padding:0.4rem 0;'>"
            "<span style='font-size:1.6rem;font-weight:700;color:#008751;'>HeedX AI</span><br>"
            "<span style='font-size:0.8rem;color:#718096;letter-spacing:0.5px;'>Nigerian Mental Health Intelligence</span>"
            "</div>",
            unsafe_allow_html=True
        )
        st.markdown("<div class='nigeria-accent'></div>", unsafe_allow_html=True)

        st.markdown("### Navigation")
        if st.button("🏠 Overview & Home", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()

        if st.button("📋 Mode A: Professional Case Analysis", use_container_width=True):
            st.session_state.page = 'mode_a'
            st.rerun()

        if st.button("💬 Mode B: Conversational Support", use_container_width=True):
            st.session_state.page = 'mode_b'
            st.rerun()

        if st.button("📍 Nigerian Support Resources", use_container_width=True):
            st.session_state.page = 'resources'
            st.rerun()

        st.markdown("---")

        # API Key Configuration
        with st.expander("🔑 Gemini API Settings", expanded=not bool(st.session_state.gemini_api_key)):
            st.caption("Required for LLM Case Formulations and Dynamic Chat.")
            new_key = st.text_input(
                "Gemini API Key",
                value=st.session_state.gemini_api_key,
                type="password",
                placeholder="AIzaSy..."
            )
            if st.button("Save API Key", use_container_width=True):
                st.session_state.gemini_api_key = new_key.strip()
                st.success("API Key saved.")

        # Crisis Emergency Quick Card
        with st.expander("🚨 Nigerian Crisis Lines", expanded=False):
            st.markdown("""
            - **National Emergency**: `112`
            - **MANI Hotline**: `08062106493`
            - **She Writes Woman**: `08099769974`
            - **Lagos State Helpline**: `767`
            """)

        # Confidentiality & Support Contacts
        st.markdown("### Confidential Connect")
        st.markdown(
            f"<a href='{CONTACT_INFO['whatsapp_link']}' target='_blank' class='contact-button contact-whatsapp'>"
            "Direct WhatsApp Support</a>",
            unsafe_allow_html=True
        )
        st.markdown(
            f"<a href='mailto:{CONTACT_INFO['email']}' class='contact-button contact-email'>"
            "Email Clinical Team</a>",
            unsafe_allow_html=True
        )

        st.caption("Privacy Guarantee: Observations and conversation data reside only within your current browser session.")


# ============================================
# PAGE 1: OVERVIEW & HOME
# ============================================
def render_home_page():
    """Landing view introducing the two-mode architecture and principles"""
    st.markdown("<h1 class='main-header'>HeedX AI</h1>", unsafe_allow_html=True)
    st.markdown("<p class='main-subtitle'>Nigerian Mental Wellness & Clinical Decision Support</p>", unsafe_allow_html=True)
    st.markdown("<p class='main-tagline'>Evidence-Grounded • Culturally Attuned • Qualitative Understanding</p>", unsafe_allow_html=True)
    st.markdown("<div class='nigeria-accent'></div>", unsafe_allow_html=True)

    col_info, col_modes = st.columns([1, 1], gap="large")

    with col_info:
        st.markdown("""
        ### Why Qualitative Understanding Matters
        Most conventional AI mental health tools attempt to compress complex human suffering into artificial percentage scores (e.g., *Depression = 78%*). Clinical mental healthcare does not operate on synthetic probabilities.

        **HeedX AI replaces artificial percentages with qualitative clinical understanding:**
        - **Presenting concerns and symptoms** extracted directly from natural language.
        - **Sociocultural context recognition** (academic strikes, economic pressures, family dynamics, stigma).
        - **Evidence grounding (RAG)** referencing peer-reviewed Nigerian epidemiological research and national surveys.
        - **Deterministic safety safeguards** guaranteeing immediate emergency contacts for acute distress.
        """)

        # Nigerian proverb banner
        proverb = random.choice(NIGERIAN_PROVERBS)
        st.info(f"💡 *Nigerian Wisdom:* \"{proverb}\"")

    with col_modes:
        st.markdown("### Choose an Operation Mode")

        # Mode A Card
        st.markdown("""
        <div class='feature-card'>
            <h4 style='color:#008751;margin-top:0;'>📋 Mode A: Professional Case Analysis</h4>
            <p style='color:#4a5568;font-size:0.92rem;'>
                Designed for psychologists, clinical researchers, counsellors, and case officers.
                Upload or paste patient notes to perform structured qualitative extraction, retrieve Nigerian clinical literature, and generate comprehensive case formulations.
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Enter Mode A (Professional)", use_container_width=True):
            st.session_state.page = 'mode_a'
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        # Mode B Card
        st.markdown("""
        <div class='feature-card'>
            <h4 style='color:#008751;margin-top:0;'>💬 Mode B: Conversational Support (User Chat)</h4>
            <p style='color:#4a5568;font-size:0.92rem;'>
                Designed for individuals seeking supportive, private conversation.
                Speak freely about what you are going through. HeedX maintains conversational context over turns and offers culturally sensitive, empathetic guidance without making clinical diagnostic claims.
            </p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Enter Mode B (Conversational Chat)", use_container_width=True):
            st.session_state.page = 'mode_b'
            st.rerun()


# ============================================
# PAGE 2: MODE A — PROFESSIONAL CASE ANALYSIS
# ============================================
def render_mode_a_page(qa_engine: QualitativeAnalysisEngine, rag_engine: RAGEngine, safety_layer: SafetyLayer):
    """
    Mode A — Professional / Case Analysis:
    - Text upload (PDF/TXT) or paste
    - Qualitative extraction (concerns, duration, functioning, stressors, risks)
    - Grounded RAG retrieval of Nigerian evidence
    - LLM-generated structured case formulation with citations
    """
    st.markdown("<h2 class='sub-header'>📋 Mode A: Professional Case Analysis</h2>", unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#4a5568;margin-top:-0.4rem;'>"
        "Qualitative clinical case formulation and evidence retrieval for mental health professionals and researchers."
        "</p>",
        unsafe_allow_html=True
    )

    col_input, col_meta = st.columns([2, 1], gap="medium")

    with col_input:
        # Document Upload
        uploaded_doc = st.file_uploader(
            "Upload clinical note or observation (.pdf, .txt)",
            type=['pdf', 'txt'],
            key=f"mode_a_uploader_{st.session_state.uploader_id}"
        )
        if uploaded_doc is not None:
            try:
                if uploaded_doc.name.endswith('.pdf'):
                    reader = pypdf.PdfReader(uploaded_doc)
                    extracted_text = "\n".join([page.extract_text() or "" for page in reader.pages])
                else:
                    extracted_text = uploaded_doc.read().decode('utf-8', errors='ignore')
                st.session_state.case_text = extracted_text.strip()
                st.success(f"Loaded '{uploaded_doc.name}' ({len(st.session_state.case_text)} characters).")
            except Exception as e:
                st.error(f"Error parsing uploaded document: {e}")

        # Direct Text Input Area
        case_input = st.text_area(
            "Patient / Client Case Observation",
            value=st.session_state.case_text,
            height=200,
            placeholder="Example: The patient reports feeling persistently sad for approximately one month. She has difficulty sleeping, has withdrawn from friends, and is struggling to concentrate at university..."
        )

        col_btn1, col_btn2 = st.columns([2, 1])
        with col_btn1:
            run_analysis = st.button("Run Qualitative Case Formulation", use_container_width=True)
        with col_btn2:
            if st.button("Clear Case", use_container_width=True):
                st.session_state.case_text = ""
                st.session_state.case_analysis = None
                st.session_state.case_evidence = []
                st.session_state.case_formulation = ""
                st.session_state.uploader_id += 1
                st.rerun()

    with col_meta:
        st.markdown("""
        <div class='clinical-card'>
            <strong>Clinical Guidelines (Mode A):</strong><br>
            • Analyzes supplied observations qualitatively.<br>
            • No synthetic percentages or probabilistic diagnoses.<br>
            • Cross-references Nigerian epidemiological studies.<br>
            • Formulates structured clinical insights for clinician decision support.
        </div>
        """, unsafe_allow_html=True)

        st.caption("Sample Case for Quick Testing:")
        if st.button("Load University Case Example", use_container_width=True):
            st.session_state.case_text = (
                "The patient is a 21-year-old female university undergraduate who reports feeling "
                "persistently sad and empty for approximately one month. She describes significant "
                "sleep difficulty, waking at 3:00 AM with racing thoughts about exams and tuition fees. "
                "She has withdrawn from her study group and stopped attending fellowship gatherings. "
                "She complains that her 'head is hot' and she cannot concentrate on lecture notes. "
                "No active suicidal plan is reported, but she expresses feeling overwhelmed and tired of life."
            )
            st.rerun()

    # Execution Pipeline
    if run_analysis:
        if not case_input.strip():
            st.warning("Please enter or upload patient text to analyze.")
            return

        st.session_state.case_text = case_input.strip()

        with st.spinner("Extracting qualitative dimensions and querying Nigerian evidence base..."):
            # Step 1: Qualitative Feature Extraction
            analysis = qa_engine.analyze(st.session_state.case_text)
            st.session_state.case_analysis = analysis

            # Step 2: Safety Check
            safety_eval = safety_layer.evaluate_message(st.session_state.case_text)

            # Step 3: Targeted RAG Retrieval
            rag_query = rag_engine.construct_query(
                current_text=st.session_state.case_text,
                concerns=analysis.get("presenting_concerns"),
                symptoms=analysis.get("symptoms_or_signals"),
                stressors=analysis.get("stressors"),
                context=analysis.get("social_context")
            )
            evidence = rag_engine.search(rag_query, top_k=3)
            st.session_state.case_evidence = evidence

            # Step 4: Structured Case Formulation via LLM
            evidence_prompt_block = rag_engine.format_evidence_for_prompt(evidence)
            system_prompt = f"""You are the HeedX Clinical Case Formulation Assistant. You assist licensed Nigerian psychologists, psychiatrists, and clinical researchers in conducting qualitative case formulation.

MANDATORY RULES:
1. Provide a rigorous, structured qualitative formulation.
2. NEVER output synthetic diagnostic percentages (e.g., do NOT output 'Depression = 78%').
3. Distinguish clearly between explicitly stated facts, semantic observations, and clinical uncertainties.
4. Reference the provided Nigerian epidemiological evidence and clinical literature where relevant.
5. Structure your output clearly according to the following sections:
   - CASE SUMMARY
   - PRESENTING CONCERNS & REPORTED SIGNALS
   - DURATION & TRAJECTORY
   - FUNCTIONAL & SOCIO-ACADEMIC IMPACT
   - STRESSORS & CONTEXTUAL FACTORS (Nigerian context)
   - RISK INDICATORS & SAFETY CONSIDERATIONS
   - PROTECTIVE FACTORS & RESILIENCE
   - RELEVANT RESEARCH EVIDENCE & GROUNDING (Cite retrieved studies)
   - SUGGESTED CLINICAL INQUIRIES FOR FURTHER ASSESSMENT
"""
            user_prompt = f"""PATIENT OBSERVATION:
{st.session_state.case_text}

STRUCTURED QUALITATIVE EXTRACTION:
- Presenting Concerns: {analysis.get('presenting_concerns')}
- Symptoms/Signals: {analysis.get('symptoms_or_signals')}
- Duration: {analysis.get('duration')}
- Stressors: {analysis.get('stressors')}
- Functional Impact: {analysis.get('functional_impact')}
- Protective Factors: {analysis.get('protective_factors')}
- Risk Signals: {analysis.get('risk_signals')}

{evidence_prompt_block}

Please generate the formal qualitative case formulation for the mental health professional."""

            formulation = call_gemini_service(
                messages=[{"role": "user", "content": user_prompt}],
                api_key=st.session_state.gemini_api_key,
                system_instruction=system_prompt,
                temperature=0.4,
                max_tokens=1200
            )
            st.session_state.case_formulation = formulation

    # Display Results if Analysis Exists
    if st.session_state.case_analysis:
        analysis = st.session_state.case_analysis
        st.markdown("---")
        st.markdown("### 1. Qualitative Information Extraction")

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("**Presenting Concerns**")
            for c in analysis.get("presenting_concerns", []):
                st.markdown(f"• {c}")
            st.markdown("**Duration**")
            st.markdown(f"• {analysis.get('duration')}")

        with c2:
            st.markdown("**Symptoms & Signals**")
            for s in analysis.get("symptoms_or_signals", []):
                st.markdown(f"• {s}")
            st.markdown("**Functional Impact**")
            for f in analysis.get("functional_impact", []):
                st.markdown(f"• {f}")

        with c3:
            st.markdown("**Stressors & Context**")
            for st_item in analysis.get("stressors", []):
                st.markdown(f"• {st_item}")
            st.markdown("**Risk Indicators**")
            risks = analysis.get("risk_signals", [])
            if risks:
                for r in risks:
                    st.markdown(f"<span style='color:#dc2626;'>⚠️ {r}</span>", unsafe_allow_html=True)
            else:
                st.markdown("• *No explicit acute crisis triggers detected in text*")

        # Grounding Evidence (RAG)
        st.markdown("### 2. Retrieved Nigerian Evidence & Clinical Guidance")
        if st.session_state.case_evidence:
            for ev in st.session_state.case_evidence:
                st.markdown(f"""
                <div class='evidence-card'>
                    <strong>{ev.get('title')}</strong> ({ev.get('year')})<br>
                    <span style='color:#4a5568;'>Source: {ev.get('source')} | Authors: {ev.get('authors')}</span><br>
                    <span style='color:#166534;'>Evidence Level: {ev.get('evidence_level')} | Population: {ev.get('population')}</span><br>
                    <p style='margin-top:0.4rem;color:#1e293b;'>{ev.get('text')}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.caption("No specific evidence records matched.")

        # Structured Case Formulation Output
        st.markdown("### 3. Comprehensive Clinical Case Formulation")
        if st.session_state.case_formulation:
            st.markdown(st.session_state.case_formulation)

            # Export / Download Case Formulation
            st.download_button(
                "📥 Download Case Formulation (.md)",
                data=f"# HeedX AI Qualitative Case Formulation\nDate: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n## Patient Observation\n{st.session_state.case_text}\n\n## Clinical Formulation\n{st.session_state.case_formulation}",
                file_name=f"heedx_case_formulation_{datetime.now().strftime('%Y%m%d_%H%M')}.md",
                mime="text/markdown",
                use_container_width=True
            )
        else:
            st.info("API key required to generate full clinical case formulation. Please set your Gemini API key in the sidebar.")


# ============================================
# PAGE 3: MODE B — CONVERSATIONAL USER MODE
# ============================================
def render_mode_b_page(
    qa_engine: QualitativeAnalysisEngine,
    rag_engine: RAGEngine,
    safety_layer: SafetyLayer,
    rec_engine: RecommendationEngine
):
    """
    Mode B — Conversational User Mode:
    - Empathetic chat interface
    - Multi-turn conversation state tracking
    - Dedicated safety layer with emergency intercept
    - Targeted RAG retrieval based on evolving conversation context
    - Grounded, non-diagnostic response generation
    """
    st.markdown("<h2 class='sub-header'>💬 Mode B: Conversational Support</h2>", unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#4a5568;margin-top:-0.4rem;'>"
        "Safe, empathetic mental wellness dialogue. HeedX listens, remembers context across turns, and offers evidence-informed support."
        "</p>",
        unsafe_allow_html=True
    )

    cstate: ConversationStateManager = st.session_state.conversation_manager

    # Display Active Safety Alert if Acute Crisis detected
    if st.session_state.active_crisis_banner:
        st.markdown(f"""
        <div class='safety-alert-card'>
            <h3 style='margin-top:0;'>🚨 Immediate Help is Available</h3>
            <p>{st.session_state.active_crisis_banner}</p>
            <strong>Verified Nigerian Emergency Support:</strong><br>
            • National Emergency: <strong>112</strong><br>
            • Mentally Aware Nigeria Initiative (MANI): <strong>08062106493</strong><br>
            • She Writes Woman Helpline: <strong>08099769974</strong><br>
            • Federal Neuropsychiatric Hospital, Yaba: <strong>08023126786</strong>
        </div>
        """, unsafe_allow_html=True)

    # Conversation State Expander (Transparent AI)
    with st.expander("🔍 Conversation Context & Themes Understood (State Tracker)", expanded=False):
        state_dict = cstate.get_state_dict()
        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1:
            st.markdown(f"**Concerns Identified:** {', '.join(state_dict['main_concerns']) or 'None yet'}")
            st.markdown(f"**Duration:** {state_dict['duration'] or 'Not specified'}")
        with col_s2:
            st.markdown(f"**Stressors:** {', '.join(state_dict['stressors']) or 'None yet'}")
            st.markdown(f"**Functional Impact:** {', '.join(state_dict['functional_impact']) or 'None yet'}")
        with col_s3:
            st.markdown(f"**Safety Status:** `{state_dict['risk_status']}`")
            st.markdown(f"**Dialogue Turns:** {cstate.turn_count}")

    # Chat Transcript Display
    chat_container = st.container()
    with chat_container:
        if not st.session_state.chat_messages:
            st.markdown("""
            <div class='chat-assistant'>
                Hello, I am HeedX. I am here to provide a safe, non-judgmental space to talk about whatever is on your mind — whether it is stress, feeling overwhelmed, sleep difficulties, or school/family pressures.<br><br>
                How have you been feeling lately?
            </div>
            """, unsafe_allow_html=True)

        for msg in st.session_state.chat_messages:
            if msg["role"] == "user":
                st.markdown(f"<div class='chat-user'>{html_lib.escape(msg['content'])}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='chat-assistant'>{msg['content']}</div>", unsafe_allow_html=True)

    # Input Form
    with st.form("mode_b_chat_form", clear_on_submit=True):
        user_message = st.text_input("Type your message here...", placeholder="Share what is on your mind...")
        col_send, col_reset = st.columns([4, 1])
        with col_send:
            submitted = st.form_submit_button("Send Message", use_container_width=True)
        with col_reset:
            reset_btn = st.form_submit_button("Reset Chat", use_container_width=True)

    if reset_btn:
        st.session_state.chat_messages = []
        st.session_state.conversation_manager.clear()
        st.session_state.active_crisis_banner = None
        st.rerun()

    if submitted and user_message.strip():
        clean_msg = user_message.strip()

        # Append user message to transcript
        st.session_state.chat_messages.append({"role": "user", "content": clean_msg})

        # Step 1: Explicit Safety Layer Triage
        safety_eval = safety_layer.evaluate_message(clean_msg)

        if safety_eval.get("is_crisis"):
            st.session_state.active_crisis_banner = (
                "You mentioned feelings of severe distress or self-harm. "
                "Your life and safety are deeply important. Please reach out to someone who can support you right now."
            )
            emergency_reply = (
                safety_eval.get("emergency_response") or
                "What you've shared indicates deep pain. You do not have to carry this alone. "
                "Please call 112 (National Emergency) or MANI on 08062106493 right now. "
                "Is there a family member, trusted friend, or doctor you can reach out to immediately?"
            )
            st.session_state.chat_messages.append({"role": "assistant", "content": emergency_reply})
            cstate.state["risk_status"] = "acute_crisis"
            st.rerun()

        # Step 2: Update Conversation State
        cstate.update_state(clean_msg, qa_engine, safety_layer)

        # Step 3: Targeted RAG Retrieval using accumulated state
        rag_query = cstate.get_retrieval_query(clean_msg)
        evidence = rag_engine.search(rag_query, top_k=2)

        # Format evidence for injection into conversational model
        evidence_block = ""
        if evidence:
            evidence_block = "RELEVANT LOCAL CLINICAL CONTEXT:\n"
            for ev in evidence:
                evidence_block += f"- {ev.get('title')}: {ev.get('text')}\n"

        # Step 4: LLM Conversational Generation
        system_instruction = f"""You are HeedX, an empathetic, culturally attuned Nigerian mental wellness companion.

CORE ETHICAL BOUNDARIES:
1. NEVER diagnose the user. Do not say 'You have depression' or 'You suffer from anxiety'.
2. Instead say: 'What you are describing includes experiences commonly associated with...' or 'These feelings often occur when carrying heavy strain.'
3. Never use emojis. Keep a warm, respectful, grounding African conversational tone.
4. Keep your response conversational and concise: between 3 and 5 sentences.
5. Empathize with their specific situation (academic strain, family, fatigue, 'head is hot', sleep).
6. Ground your response in healthy coping, and ask ONE thoughtful, open question to help them reflect.

{evidence_block}

CURRENT CONVERSATION STATE:
- Main Concerns: {cstate.state['main_concerns']}
- Duration: {cstate.state['duration']}
- Stressors: {cstate.state['stressors']}
- Functional Impact: {cstate.state['functional_impact']}
"""
        # Prepare message history for Gemini (last 8 turns for efficiency)
        gemini_messages = []
        for m in st.session_state.chat_messages[-8:]:
            gemini_messages.append({
                "role": "user" if m["role"] == "user" else "assistant",
                "content": m["content"]
            })

        assistant_reply = call_gemini_service(
            messages=gemini_messages,
            api_key=st.session_state.gemini_api_key,
            system_instruction=system_instruction,
            temperature=0.6,
            max_tokens=350
        )

        st.session_state.chat_messages.append({"role": "assistant", "content": assistant_reply})
        st.rerun()


# ============================================
# PAGE 4: NIGERIAN RESOURCES DIRECTORY
# ============================================
def render_resources_page():
    """Comprehensive, deterministic directory of verified Nigerian mental health resources"""
    st.markdown("<h2 class='sub-header'>📍 Nigerian Mental Health Resources Directory</h2>", unsafe_allow_html=True)
    st.markdown(
        "<p style='color:#4a5568;margin-top:-0.4rem;'>"
        "Verified, deterministic contacts, emergency services, psychiatric hospitals, and community helplines across Nigeria."
        "</p>",
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("### 🚨 Emergency & Crisis Hotlines")
        st.markdown("""
        - **National Emergency Number**: `112` (Toll-free from any network)
        - **Lagos State Emergency**: `767` or `112`
        - **Mentally Aware Nigeria Initiative (MANI)**:
          - Phone: `08062106493` / `08091116264`
          - Focus: 24/7 Crisis triage, youth mental health, suicide prevention.
        - **She Writes Woman**:
          - Phone: `08099769974`
          - Focus: Confidential 24/7 mental health crisis hotline.
        - **Nigeria Suicide Prevention Helpline**: `08062106493`
        """)

        st.markdown("### 🤝 Faith & Community Support")
        for org, details in FAITH_COMMUNITY_SUPPORT.items():
            st.markdown(f"**{org.replace('_', ' ').title()}**")
            st.markdown(f"- *Phone:* `{details['phone']}`")
            st.markdown(f"- *Support:* {details['approach']}")

    with c2:
        st.markdown("### 🏥 Federal Neuropsychiatric Hospitals")
        st.markdown("""
        - **Federal Neuropsychiatric Hospital, Yaba (Lagos)**
          - Address: Harvey Road, Yaba, Lagos State
          - Phone: `08023126786`
        - **Neuropsychiatric Hospital, Aro, Abeokuta (Ogun State)**
          - Address: Aro, Abeokuta, Ogun State
          - Phone: `08033333333` (Hospital Registry)
        - **Federal Neuropsychiatric Hospital, Barnawa (Kaduna State)**
          - Address: Barnawa, Kaduna State
        - **Federal Neuropsychiatric Hospital, Uselu (Benin City, Edo State)**
          - Address: Uselu, Benin City
        - **Federal Neuropsychiatric Hospital, Calabar (Cross River State)**
          - Address: Calabar Road, Calabar
        - **Federal Neuropsychiatric Hospital, Kware (Sokoto State)**
          - Address: Kware, Sokoto State
        """)

        st.markdown("### 🌿 Evidence-Based Nigerian Wellness Tips")
        for category, tips in CULTURAL_WELLNESS_TIPS.items():
            with st.expander(tips['title']):
                st.write(tips['message'])
                for i, tip in enumerate(tips['tips'], 1):
                    st.write(f"{i}. {tip}")


# ============================================
# MAIN APPLICATION CONTROLLER
# ============================================
def main():
    """Main application lifecycle and routing"""
    init_session_state()

    qa_engine, rag_engine, safety_layer, rec_engine = get_shared_core()

    # Development Notice
    st.info(
        "🛡️ **HeedX AI 2.0**: Redesigned around the Two-Mode Architecture — "
        "**Mode A (Professional Case Analysis)** and **Mode B (Conversational Support)** with a shared RAG and safety layer."
    )

    # Render Persistent Sidebar
    render_sidebar()

    # Page Dispatch
    current_page = st.session_state.page

    if current_page == 'home':
        render_home_page()
    elif current_page == 'mode_a':
        render_mode_a_page(qa_engine, rag_engine, safety_layer)
    elif current_page == 'mode_b':
        render_mode_b_page(qa_engine, rag_engine, safety_layer, rec_engine)
    elif current_page == 'resources':
        render_resources_page()
    else:
        render_home_page()

    # Footer
    st.markdown("---")
    st.markdown("""
    <div class='disclaimer'>
        <p><strong>HeedX AI &mdash; Nigerian Edition 2.0</strong></p>
        <p>HeedX provides qualitative support, semantic analysis, and evidence-grounded information. It does not provide definitive medical or psychiatric diagnoses.</p>
        <p>Crisis Lines: <strong>112</strong> (National Emergency) &nbsp;|&nbsp; <strong>08062106493</strong> (MANI) &nbsp;|&nbsp; <strong>08099769974</strong> (She Writes Woman)</p>
        <p>You are never alone. Help and community are always available.</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
