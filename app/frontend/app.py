import streamlit as st
import requests
import json
import time

API_URL = "http://localhost:8000/api/v1"
IDLE_TIMEOUT = 20  # in seconds 

def init_session_state():
    if 'code_input' not in st.session_state:
        st.session_state.code_input = ""
    if 'last_interaction' not in st.session_state:
        st.session_state.last_interaction = time.time()
    if 'action' not in st.session_state:
        st.session_state.action = None
    if 'problem_statement' not in st.session_state:
        st.session_state.problem_statement = ""

def display_code(code: str, language: str):
    st.code(code, language=language)

def get_suggestions(code_input):
    try:
        response = requests.post(f"{API_URL}/get_suggestions", json={"code": code_input})
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        result = response.json()
        return result
    except requests.exceptions.RequestException as e:
        st.error(f"Error getting suggestions: {e}")
        return None
    except json.JSONDecodeError as e:
        st.error(f"Error decoding suggestions response: {e}")
        return None

def main():
    st.set_page_config(page_title="Code Mentor Bot", layout="wide")
    init_session_state()

    st.title("🤖 Code Mentor Bot")
    col1, col2 = st.columns([1, 1])

    with col1:
        problem_statement = st.text_area("Enter problem statement here (optional)", value=st.session_state.problem_statement, height=150, key="problem_statement")
        code_input = st.text_area("Enter your code here", value=st.session_state.code_input, height=300, key="code_input")

        col1_action, col2_action, col3_action, col4_action = st.columns(4)
        actions = ["Debug Code", "Convert Code", "Analyze Complexity", "Get Suggestions"]

        def action_button(col, action_name):
            if col.button(action_name, use_container_width=True):
                st.session_state.action = action_name
                st.session_state.last_interaction = time.time()  # Reset timer

        action_button(col1_action, actions[0])
        action_button(col2_action, actions[1])
        action_button(col3_action, actions[2])
        action_button(col4_action, actions[3])

        if st.session_state.action == "Convert Code":
            col_source, col_target = st.columns(2)
            with col_source:
                source_language = st.selectbox("Source Language", ["python", "javascript", "java", "cpp"], key="source_language")
            with col_target:
                target_language = st.selectbox("Target Language", ["python", "javascript", "java", "cpp"], key="target_language")
            process_button = st.button("Process", type="primary")
        else:
            source_language = None
            target_language = None
            process_button = True

    # Idle timeout logic
    if time.time() - st.session_state.last_interaction > IDLE_TIMEOUT and st.session_state.action != "Convert Code":
        st.session_state.action = "Get Suggestions"
        # st.info("No activity detected. Automatically getting suggestions...")

    with col2:
        if st.session_state.action:
            with st.spinner(f"Processing {st.session_state.action}..."):
                try:
                    combined_input = f"Problem Statement: {problem_statement}\nCode: {code_input}"

                    if st.session_state.action == "Debug Code":
                        response = requests.post(f"{API_URL}/debug", json={"code": combined_input})
                        result = response.json()
                        st.markdown("### Debug Results")
                        if "summary" in result:
                            st.info(result["summary"])
                        if "issues" in result and result["issues"]:
                            st.markdown("#### Issues Found")
                            for issue in result["issues"]:
                                with st.expander(f"Issue at Line {issue['line']} - {issue['type']}", expanded=True):
                                    st.markdown(f"**Description:** {issue['description']}")
                                    st.markdown(f"**Suggestion:** {issue['suggestion']}")
                        if "fixed_code" in result:
                            st.markdown("#### Fixed Code")
                            display_code(result["fixed_code"], "python")

                    elif st.session_state.action == "Convert Code" and process_button:
                        if not source_language or not target_language:
                            st.error("Please select source and target languages.")
                        else:
                            response = requests.post(f"{API_URL}/convert", json={"code": combined_input, "source_lang": source_language, "target_lang": target_language})
                            result = response.json()
                            st.markdown("### Conversion Results")
                            if "summary" in result:
                                st.info(result["summary"])
                            if "changes" in result and result["changes"]:
                                st.markdown("#### Changes Made")
                                for change in result["changes"]:
                                    with st.expander(change["description"], expanded=True):
                                        st.markdown(change["note"])
                            if "converted_code" in result:
                                st.markdown("#### Converted Code")
                                display_code(result["converted_code"], target_language)

                    elif st.session_state.action == "Analyze Complexity":
                        response = requests.post(f"{API_URL}/analyze-complexity", json={"code": combined_input})
                        result = response.json()
                        st.markdown("### Complexity Analysis")
                        if "summary" in result:
                            st.info(result["summary"])
                        if "time_complexity" in result:
                            with st.expander("Time Complexity", expanded=True):
                                st.markdown(f"**Overall: {result['time_complexity']['overall']}**")
                                st.markdown(result['time_complexity']['explanation'])
                                if result['time_complexity'].get('breakdown'):
                                    st.markdown("#### Detailed Breakdown")
                                    for section in result['time_complexity']['breakdown']:
                                        st.markdown(f"**{section['section']}:** {section['complexity']}")
                                        st.markdown(section['explanation'])
                        if "space_complexity" in result:
                            with st.expander("Space Complexity", expanded=True):
                                st.markdown(f"**Overall: {result['space_complexity']['overall']}**")
                                st.markdown(result['space_complexity']['explanation'])
                        if "optimization_suggestions" in result and result["optimization_suggestions"]:
                            with st.expander("Optimization Suggestions", expanded=True):
                                for suggestion in result["optimization_suggestions"]:
                                    st.markdown(f"**Suggestion:** {suggestion['description']}")
                                    st.markdown(f"**Expected Impact:** {suggestion['impact']}")

                    elif st.session_state.action == "Get Suggestions":
                        suggestions = get_suggestions(combined_input)
                        if suggestions:
                            st.markdown("### Suggestions")
                            st.write(suggestions)

                except Exception as e:
                    st.error(f"Error: {e}")

    st.session_state.last_interaction = time.time()  # Update interaction time after processing

if __name__ == "__main__":
    main()
