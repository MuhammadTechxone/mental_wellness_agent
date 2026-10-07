# HeedX AI — Streamlit Community Cloud Deployment Guide

## Pre-Deployment Checklist

✅ **All legacy classifier references removed**  
✅ **Two-mode architecture (Mode A + Mode B) active**  
✅ **RAG system with knowledge base loaded**  
✅ **Safety layer independent and deterministic**  
✅ **Nigerian resources directory included**  
✅ **No benchmark/research page**  
✅ **No PHQ-9/GAD-7 questionnaire flow**  
✅ **Conversation state tracking functional**  
✅ **Gemini API integration ready**  

---

## Deployment to Streamlit Community Cloud

### Step 1: Prepare Your Repository

Ensure the repository is public and contains:
```
mental_health_app_real/
├── mental_app.py              # Main Streamlit app
├── requirements.txt           # Dependencies (NO joblib, NO scikit-learn)
├── verify_migration.py        # Validation script
├── config/
│   └── settings.py            # Configuration (empty QUESTIONNAIRE, MENTAL_HEALTH_CLASSES)
├── utils/
│   ├── qualitative_engine.py  # Qualitative analysis (production)
│   ├── rag_engine.py          # RAG system
│   ├── safety_layer.py        # Safety layer
│   ├── conversation_state.py  # State tracking
│   ├── recommendations.py     # Recommendation engine
│   ├── preprocessing.py       # Text preprocessing
│   ├── lexicons.py            # Lexicon data
│   └── session_storage.py     # Session tracking
├── knowledge/                 # Knowledge base (JSON/Markdown)
│   ├── knowledge_store.json
│   ├── nigeria_evidence/
│   ├── nigeria_context/
│   ├── psychoeducation/
│   └── scenarios/
├── .streamlit/
│   ├── config.toml            # Streamlit theme & server config
│   └── secrets.toml.example   # Example secrets template
└── README.md, OVERVIEW_FOR_USERS.md, DEVELOPMENT_STEPS.md
```

### Step 2: Update requirements.txt

Remove:
- ❌ `joblib` (used only for old SVM model)
- ❌ `scikit-learn` (used only for TF-IDF + SVM)
- ❌ `plotly` (not needed in production mode)
- ❌ `plotly.express`

Keep:
```
streamlit>=1.31.0
pandas>=2.0.0
numpy>=1.24.0
requests>=2.31.0
pypdf>=3.17.0
google-generativeai>=0.3.0
```

### Step 3: Create Streamlit Configuration

Create `.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#008751"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f8f9fa"
textColor = "#1a202c"
font = "sans serif"

[client]
showErrorDetails = false
showWarningOnDirectExecution = false

[server]
maxUploadSize = 50
enableXsrfProtection = true
headless = true
```

### Step 4: Manage Secrets

Create `.streamlit/secrets.toml.example` for documentation:
```toml
# Copy this file to .streamlit/secrets.toml and add your actual API key
# DO NOT commit secrets.toml to version control

GEMINI_API_KEY = "your_gemini_api_key_here"
```

**In Streamlit Cloud Dashboard:**
1. Go to your app settings
2. Click "Secrets"
3. Paste your actual Gemini API key:
   ```
   GEMINI_API_KEY = "AIzaSy..."
   ```

### Step 5: Deploy to Streamlit Community Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Select your repository: `MuhammadTechxone/mental_wellness_agent`
4. Branch: `main`
5. Main file path: `mental_health_app_real/mental_app.py`
6. Click "Deploy"

### Step 6: Configure Secrets in Streamlit Cloud

After deployment:
1. Click on your app settings (gear icon)
2. Go to "Secrets"
3. Add your Gemini API key
4. Redeploy

---

## Post-Deployment Validation

### Test Mode A (Professional Case Analysis)
1. Click "Mode A: Professional Case Analysis"
2. Use the example case loader
3. Click "Run Qualitative Case Formulation"
4. Verify:
   - ✅ Qualitative extraction displays
   - ✅ Evidence retrieval shows Nigerian studies
   - ✅ Case formulation generates via Gemini
   - ✅ Download button works

### Test Mode B (Conversational Support)
1. Click "Mode B: Conversational Support"
2. Type a test message: "I've been feeling sad lately"
3. Click "Send Message"
4. Verify:
   - ✅ Response is conversational (not diagnostic)
   - ✅ State tracker shows concerns
   - ✅ No diagnostic percentages appear
   - ✅ Multiple turns work smoothly

### Test Crisis Detection
1. In Mode B, type: "I want to die"
2. Verify:
   - ✅ Crisis banner appears immediately
   - ✅ Emergency contacts display
   - ✅ Response indicates crisis pathway

### Test Resources Page
1. Click "Nigerian Support Resources"
2. Verify:
   - ✅ Emergency hotlines display
   - ✅ Hospital directories show
   - ✅ Faith and community resources listed
   - ✅ All numbers are clickable/copyable

---

## Monitoring & Troubleshooting

### Common Issues

**Issue:** "Gemini API key is not configured"
- **Solution:** Check Streamlit Cloud secrets. Go to app settings → Secrets and verify `GEMINI_API_KEY` is set.

**Issue:** "ModuleNotFoundError: No module named 'sklearn'"
- **Solution:** Verify `requirements.txt` does NOT include `scikit-learn`. Remove it if present.

**Issue:** "ModuleNotFoundError: No module named 'joblib'"
- **Solution:** Verify `requirements.txt` does NOT include `joblib`. Remove it if present.

**Issue:** Knowledge base not loading
- **Solution:** Verify `knowledge/knowledge_store.json` exists in the repo. RAGEngine loads it at startup.

**Issue:** Slow performance on first load
- **Solution:** First load caches the shared core (QA engine, RAG, safety layer). Subsequent loads are fast. This is expected.

### View Logs

In Streamlit Cloud:
1. Click your app
2. Click "Manage app" (settings gear)
3. Click "Logs"
4. Check for errors during startup and runtime

---

## Performance Optimization

### Already Implemented
- ✅ `@st.cache_resource` for shared core (loaded once, reused across sessions)
- ✅ Focused RAG queries (not blind embedding of entire conversations)
- ✅ Streaming Gemini responses (via REST API with efficient payloads)
- ✅ Minimal state management (only essentials tracked)

### Streamlit Cloud Limits
- Memory: ~1 GB per app instance
- CPU: Shared resources
- Execution: Reruns on user interaction (expected behavior)
- Storage: Limited (knowledge base loaded from repo)

---

## Security & Privacy

### Data Handling
- ✅ No data persisted to databases
- ✅ Conversation data stays in browser session only
- ✅ Gemini API calls are the only external data flow
- ✅ Secrets stored securely in Streamlit Cloud
- ✅ HTTPS enforced
- ✅ No cookies or tracking

### API Security
- ✅ Gemini API key stored in Streamlit secrets (not in code)
- ✅ API key never logged or displayed
- ✅ XSRF protection enabled
- ✅ File upload size limited to 50 MB

---

## Maintenance

### Regular Tasks
- Monitor Gemini API usage in Google Cloud Console
- Check Streamlit Cloud logs for errors
- Update dependencies monthly
- Test all modes weekly
- Validate knowledge base is loading

### Update Procedure
1. Make changes locally
2. Test with `streamlit run mental_app.py`
3. Commit to `main` branch
4. Streamlit Cloud auto-redeploys
5. Verify all modes work post-deploy

---

## Support & Escalation

### If Crisis Detection Fails
- Safety layer has explicit regex patterns for crisis triggers
- If a crisis message is not detected, check `utils/safety_layer.py` CRISIS_TRIGGERS
- Add missing patterns and redeploy

### If Gemini API Fails
- App has fallback text
- Check Gemini API quota in Google Cloud Console
- Verify API key is correct in Streamlit secrets
- Check network connectivity in Streamlit Cloud logs

### For Questions or Issues
- Check `OVERVIEW_FOR_USERS.md` for user-facing documentation
- Check `DEVELOPMENT_STEPS.md` for technical architecture
- Check `improvement.md` for roadmap and future directions
- Review `README.md` for deployment checklist

---

**HeedX AI is now production-ready for Streamlit Community Cloud deployment.**

Version 2.0 — Fully Migrated to Two-Mode Architecture.
