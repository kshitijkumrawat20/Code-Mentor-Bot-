import streamlit as st
import requests
import json
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
import pygments.lexers

API_URL = "http://localhost:8000/api/v1"

def init_session_state():
    if 'code_input' not in st.session_state:
        st.session_state.code_input = ""
    if 'selected_language' not in st.session_state:
        st.session_state.selected_language = "python"

def display_code(code: str, language: str):
    # Ensure code is a string
    if not isinstance(code, str):
        code = str(code)
    
    try:
        lexer = get_lexer_by_name(language, stripall=True)
        formatter = HtmlFormatter(style='monokai', cssclass='syntax-highlight')
        highlighted = highlight(code, lexer, formatter)
        
        # Include CSS for syntax highlighting
        st.markdown(f"""
            <style>
                .syntax-highlight {{ background-color: #272822; padding: 10px; border-radius: 5px; }}
                {formatter.get_style_defs('.syntax-highlight')}
            </style>
            {highlighted}
        """, unsafe_allow_html=True)
    except Exception as e:
        # Fallback to regular code display if highlighting fails
        st.code(code, language=language)

def main():
    st.set_page_config(page_title="Code Mentor Bot", layout="wide")
    init_session_state()

    st.title("🤖 Code Mentor Bot")
    
    # Sidebar
    st.sidebar.header("Settings")
    action = st.sidebar.selectbox(
        "Select Action",
        ["Debug Code", "Convert Code", "Analyze Complexity"]
    )

    # Main content
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
                        
                        # Display debug summary
                        st.markdown("### Debug Summary")
                        st.write(result.get("summary", "No summary available"))
                        
                        # Display issues
                        st.markdown("### Issues Found")
                        issues = result.get("issues", [])
                        if issues:
                            for issue in issues:
                                severity_color = {
                                    "high": "🔴",
                                    "medium": "🟡",
                                    "low": "🟢"
                                }.get(issue["severity"], "⚪")
                                
                                st.markdown(f"""
                                    {severity_color} **Line {issue['line']} - {issue['type']}**  
                                    Description: {issue['description']}  
                                    Suggestion: {issue['suggestion']}
                                """)
                        else:
                            st.success("No issues found in the code!")
                        
                        # Store the result for the other column
                        st.session_state.result = result.get("fixed_code", "")
                        
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
                        # Store the result for the other column
                        st.session_state.result = result.get("converted_code", "")
                        
                    elif action == "Analyze Complexity":
                        response = requests.post(
                            f"{API_URL}/analyze-complexity",
                            json={"code": code_input}
                        )
                        st.session_state.result = response.json()

                except Exception as e:
                    st.error(f"Error: {str(e)}")

    with col2:
        st.markdown("### Output")
        if hasattr(st.session_state, 'result'):
            if action == "Analyze Complexity":
                st.markdown("#### Time Complexity")
                st.info(st.session_state.result.get("time_complexity", "N/A"))
                
                st.markdown("#### Space Complexity")
                st.info(st.session_state.result.get("space_complexity", "N/A"))
                
                st.markdown("#### Explanation")
                st.write(st.session_state.result.get("explanation", "No explanation available"))
            else:
                if isinstance(st.session_state.result, str) and st.session_state.result.strip():
                    display_code(
                        st.session_state.result,
                        target_language if action == "Convert Code" else source_language
                    )
                else:
                    st.warning("No output generated")

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center'>
            <p>Built with ❤️ using FastAPI, CodeT5, and Streamlit</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()