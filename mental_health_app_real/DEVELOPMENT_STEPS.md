# 🛠️ Technical Process Overview: HeedX AI Pipeline

This document outlines the end-to-end technical flow of the HeedX AI system, serving as the baseline for future intelligence improvements.

## Step 1: Input Acquisition
*   **Questionnaire Interface**: Collects multi-faceted user input across six specific psychological dimensions (Mood, Stress, Energy, Social, Outlook, General).
*   **Data Capture**: Responses are stored temporarily in the Streamlit Session State.

## Step 2: Text Preprocessing & Segmentation
*   **Normalization**: Text is lowercased and stripped of excessive noise (special characters/digits) to match training data conditions.
*   **Sentence Splitting**: Uses a robust Regex-based splitter to break long responses into individual analytical units. This allows for granular detection of conflicting emotions.

## Step 3: Classical ML Inference (The Classifier)
*   **Vectorization**: Sentences are converted into numerical features using the internal pipeline logic.
*   **SVM Prediction**: A Support Vector Machine (SVC) model classifies each sentence into one of four classes: `Normal`, `Anxiety`, `Depression`, or `Suicidal`.
*   **Confidence Scoring**: The model calculates the probability of each classification, flagging results with low confidence for "Review."

## Step 4: Analytical Aggregation
*   **Indicator Distribution**: Calculates the percentage of the total input belonging to each class.
*   **Primary/Secondary Identification**: Determines the dominant emotional states.
*   **Risk Level Calculation**: 
    *   Applies a logic-based threshold system (defined in `settings.py`).
    *   Priority Flagging: If even a single sentence is flagged as `Suicidal`, the system triggers specific safety protocols regardless of other scores.

## Step 5: Recommendation Engine
*   **Contextual Mapping**: Maps the identified Risk Level and Primary Indicator to a library of culturally adapted Nigerian wellness tips.
*   **Resource Delivery**: Dynamically displays emergency contacts and professional support based on the calculated risk.

## Step 6: Conversational Context (The Chatbot)
*   **Context Injection**: The results of the Classical ML analysis are formatted into a "System Prompt" for the Llama-3 model.
*   **Informed Dialogue**: This allows the chatbot to "know" the user's assessment results without the user having to repeat themselves, bridging the gap between rigid classification and fluid conversation.

## Future Intelligence Deliberation
*   **Logic Enhancement**: Refining how the system weighs specific keywords vs. sentence structure.
*   **Trend Integration**: Improving the logic that tracks changes between different check-ins in the same session.
*   **Refinement of Risk Thresholds**: Adjusting the "Moderate" vs "High" risk triggers based on user testing data.

---
*Next Steps: We will iterate on the Step 4 logic to better handle nuanced linguistic patterns common in Nigerian English (Pidgin/Local phrasing).*