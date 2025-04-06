# Top of app.py (BEFORE any other imports)
import sys
import collections

# Fix for Python 3.11+ compatibility
if sys.version_info >= (3, 11):
    collections.Mapping = collections.abc.Mapping
    collections.Sequence = collections.abc.Sequence
    collections.Iterable = collections.abc.Iterable

# SQLite3 fix for Streamlit
__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

# Now import other dependencies
from experta import *
from mental_health_expert import MentalHealthExpert
import streamlit as st

# Define the questions
questions = [
    {'key': 'feeling_down', 'text': '1. Do you often feel down, depressed, or hopeless?'},
    {'key': 'loss_interest', 'text': '2. Have you lost interest in daily activities?'},
    {'key': 'sleep_issues', 'text': '3. Do you have significant sleep problems?'},
    {'key': 'energy_loss', 'text': '4. Do you often feel fatigued or low-energy?'},
    {'key': 'anxiety', 'text': '5. Do you experience excessive anxiety or worry?'},
    {'key': 'panic_attacks', 'text': '6. Have you had sudden panic attacks?'},
    {'key': 'social_avoidance', 'text': '7. Do you avoid social interactions?'},
    {'key': 'trauma_history', 'text': '8. Have you experienced traumatic events?'},
    {'key': 'compulsive_behavior', 'text': '9. Do you repeat rituals to reduce anxiety?'},
    {'key': 'mood_swings', 'text': '10. Do you experience extreme mood swings?'},
]

def main():
    st.title("🧠 Mental Wellness Assessment")
    st.markdown("Please answer the following questions with **Yes** or **No**.")

    # Initialize session state for answers if they are not set
    for q in questions:
        if q['key'] not in st.session_state:
            st.session_state[q['key']] = None

    # Display questions and get responses
    for q in questions:
        st.radio(
            q['text'],
            options=['yes', 'no'],
            format_func=lambda x: x.capitalize(),
            key=q['key']
        )

    # Check if all questions are answered
    all_answered = all(st.session_state[q['key']] is not None for q in questions)

    if all_answered and st.button('Submit for Analysis'):
        # Initialize expert system
        expert = MentalHealthExpert()
        expert.reset()

        # Capture printed output
        output = StringIO()
        with redirect_stdout(output):
            expert.declare(Fact(action='assess_mental_health'))  # Add general assessment action
            # Declare each fact based on answers
            for q in questions:
                # Map 'yes' to True and 'no' to False for fact declaration
                expert.declare(Fact(**{q['key']: True if st.session_state[q['key']] == 'yes' else False}))
            expert.run()

        # Display results
        st.subheader("Assessment Results")
        result_text = output.getvalue()
        st.write(result_text)

        # Crisis alert formatting
        if "Severe" in result_text:
            st.error("Immediate professional consultation required!")
            st.markdown("🔔 National Suicide Prevention Lifeline: 1-800-273-TALK (8255)")

        # Restart option
        if st.button("Start New Assessment"):
            # Reset session state for answers
            for q in questions:
                del st.session_state[q['key']]
            st.experimental_rerun()

if __name__ == "__main__":
    main()
