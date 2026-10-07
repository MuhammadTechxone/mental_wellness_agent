import sys

try:
    print("Testing module imports...")
    import config.settings
    import utils.preprocessing
    import utils.lexicons
    import utils.analysis
    import utils.recommendations
    import utils.session_storage
    import utils.qualitative_engine
    import utils.rag_engine
    import utils.safety_layer
    import utils.conversation_state
    print("All utils and config imported successfully!")

    import mental_app
    print("mental_app.py imported and parsed cleanly!")

    # Verify instantiation of shared core
    qa = utils.qualitative_engine.QualitativeAnalysisEngine()
    rag = utils.rag_engine.RAGEngine()
    safety = utils.safety_layer.SafetyLayer()
    cstate = utils.conversation_state.ConversationStateManager()
    rec = utils.recommendations.RecommendationEngine()

    print(f"RAG loaded {len(rag.chunks)} chunks from knowledge base.")
    
    # Test qualitative recommendations
    test_analysis = {
        "presenting_concerns": ["sleep difficulty", "academic burnout"],
        "symptoms_or_signals": ["low mood", "exhaustion"],
        "stressors": ["university exams"]
    }
    recs = rec.get_qualitative_recommendations(test_analysis)
    print(f"Generated {len(recs['tips'])} qualitative recommendation tips.")

    print("ALL MIGRATION VERIFICATION CHECKS PASSED!")
except Exception as e:
    print("VERIFICATION FAILED:", e)
    import traceback
    traceback.print_exc()
    sys.exit(1)
