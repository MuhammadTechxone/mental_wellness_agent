import sys

try:
    print("Testing migration-critical imports...")
    import config.settings
    import utils.preprocessing
    import utils.lexicons
    import utils.qualitative_engine
    import utils.rag_engine
    import utils.safety_layer
    import utils.conversation_state
    import utils.recommendations
    print("Core migration modules imported successfully!")

    import mental_app
    print("mental_app.py imported and parsed cleanly!")

    qa = utils.qualitative_engine.QualitativeAnalysisEngine()
    rag = utils.rag_engine.RAGEngine()
    safety = utils.safety_layer.SafetyLayer()
    cstate = utils.conversation_state.ConversationStateManager()
    rec = utils.recommendations.RecommendationEngine()

    test_analysis = {
        "presenting_concerns": ["sleep difficulty", "academic pressure"],
        "symptoms_or_signals": ["low mood", "exhaustion"],
        "stressors": ["university exams"]
    }
    recs = rec.get_qualitative_recommendations(test_analysis)
    print(f"Generated {len(recs['tips'])} qualitative recommendation tips.")
    print(f"RAG loaded {len(rag.chunks)} chunks from the knowledge base.")

    safety_eval = safety.evaluate_message("I want to die")
    print(f"Safety triage active: {safety_eval['is_crisis']}")

    state = cstate.update_state("I have not been sleeping well and I am overwhelmed by my studies.", qa, safety)
    print(f"Conversation state updated: {state['main_concerns']}")

    print("ALL MIGRATION VERIFICATION CHECKS PASSED!")
except Exception as e:
    print("VERIFICATION FAILED:", e)
    import traceback
    traceback.print_exc()
    sys.exit(1)
