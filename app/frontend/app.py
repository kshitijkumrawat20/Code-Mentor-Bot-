import streamlit as st
import requests
import json
import re

API_URL = "https://8000-01jhhtxvxgjdvd7s8crb29884b.cloudspaces.litng.ai/api/v1"

def init_session_state():
    if 'code_input' not in st.session_state:
        st.session_state.code_input = ""
    if 'selected_language' not in st.session_state:
        st.session_state.selected_language = "python"

def display_code(code: str, language: str):
    """Display code with proper formatting in Streamlit"""
    if not code:
        return
    
    # Remove any HTML tags if present in the code
    code = re.sub(r'<[^>]+>', '', code)
    
    # Use Streamlit's built-in code display
    st.code(code, language=language)

def main():
    st.set_page_config(page_title="Code Mentor Bot", layout="wide")
    init_session_state()

    st.title("🤖 Code Mentor Bot")
    
    st.sidebar.header("Settings")
    action = st.sidebar.selectbox(
        "Select Action",
        ["Debug Code", "Convert Code", "Analyze Complexity"]
    )

    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### Input Code")
        code_input = st.text_area(
            "Enter your code here",
            value=st.session_state.code_input,
            height=300,
            key="code_input"
        )

        source_language = st.selectbox(
            "Source Language",
            ["python", "javascript", "java", "cpp"],
            key="source_language"
        )

        if action == "Convert Code":
            target_language = st.selectbox(
                "Target Language",
                [lang for lang in ["python", "javascript", "java", "cpp"] if lang != source_language],
                key="target_language"
            )

        if st.button("Process", type="primary"):
            with st.spinner("Processing..."):
                try:
                    if action == "Debug Code":
                        response = requests.post(
                            f"{API_URL}/debug",
                            json={"code": code_input}
                        )
                        result = response.json()
                        
                        with col2:
                            st.markdown("### Debug Results")
                            
                            if "summary" in result:
                                st.markdown("#### Summary")
                                st.info(result["summary"])
                            
                            if "issues" in result and result["issues"]:
                                st.markdown("#### Issues Found")
                                for issue in result["issues"]:
                                    with st.expander(f"Issue at Line {issue['line']} - {issue['type']}", expanded=True):
                                        st.markdown(f"**Description:** {issue['description']}")
                                        st.markdown(f"**Suggestion:** {issue['suggestion']}")
                            
                            if "fixed_code" in result and result["fixed_code"]:
                                st.markdown("#### Fixed Code")
                                display_code(result["fixed_code"], source_language)
                        
                    elif action == "Convert Code":
                        response = requests.post(
                            f"{API_URL}/convert",
                            json={
                                "code": code_input,
                                "source_lang": source_language,
                                "target_lang": target_language
                            }
                        )
                        result = response.json()
                        with col2:
                            st.markdown("### Conversion Results")
                            
                            if "summary" in result:
                                st.markdown("#### Summary")
                                st.info(result["summary"])
                            
                            if "changes" in result and result["changes"]:
                                st.markdown("#### Changes Made")
                                for change in result["changes"]:
                                    with st.expander(change["description"], expanded=True):
                                        st.markdown(change["note"])
                            
                            if "converted_code" in result and result["converted_code"]:
                                st.markdown("#### Converted Code")
                                display_code(result["converted_code"], target_language)
                        
                    elif action == "Analyze Complexity":
                        response = requests.post(
                            f"{API_URL}/analyze-complexity",
                            json={"code": code_input}
                        )
                        result = response.json()
                        with col2:
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

                except Exception as e:
                    st.error(f"Error: {str(e)}")

    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center'>
            <p>Built with ❤️ using FastAPI, QwenCoderModel, and Streamlit</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
