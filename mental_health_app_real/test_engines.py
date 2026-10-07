import sys
import os

try:
    from utils.qualitative_engine import QualitativeAnalysisEngine
    from utils.rag_engine import RAGEngine
    from utils.safety_layer import SafetyLayer
    from utils.conversation_state import ConversationStateManager

    qa = QualitativeAnalysisEngine()
    rag = RAGEngine()
    safety = SafetyLayer()
    cstate = ConversationStateManager()

    test_text = "Patient reports feeling sad most days for the past month, has stopped enjoying social activities and is having difficulty sleeping. Academic workload has increased significantly."
    analysis = qa.analyze(test_text)
    print("QA Concerns:", analysis.get("presenting_concerns"))
    print("QA Symptoms:", analysis.get("symptoms_or_signals"))
    print("QA Duration:", analysis.get("duration"))
    print("QA Stressors:", analysis.get("stressors"))

    query = rag.construct_query(test_text, concerns=analysis.get("presenting_concerns"), symptoms=analysis.get("symptoms_or_signals"), stressors=analysis.get("stressors"))
    results = rag.search(query, top_k=2)
    print("RAG top result:", results[0]["title"] if results else "None")

    safe_check = safety.evaluate_message(test_text)
    print("Safety Check:", safe_check["risk_level"])

    crisis_text = "I want to kill myself, I cannot go on"
    crisis_eval = safety.evaluate_message(crisis_text)
    print("Crisis Check:", crisis_eval["risk_level"], crisis_eval["is_crisis"])

    cstate.update_state("I have been feeling down lately", qa, safety)
    cstate.update_state("It has been about three weeks and I cannot sleep", qa, safety)
    cstate.update_state("University has also been stressful", qa, safety)
    print("Conversation State:", cstate.get_state_dict())
    print("ALL TESTS PASSED SUCCESSFULLY!")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
