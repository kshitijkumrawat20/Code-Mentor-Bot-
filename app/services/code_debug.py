import json
from app.models.code_model import QwenCoderModel

class CodeDebugger:
    def __init__(self):
        self.model = QwenCoderModel()

    def debug_code(self, code: str) -> dict:
        # Create a more structured prompt that explicitly asks for JSON format
        prompt = f"""You are a helpful code mentor bot. Analyze the following code and respond with ONLY a JSON object in the exact format shown below, with no additional text or explanation:

{{
  "issues": [
    {{
      "line": <integer>,
      "type": "<string: SyntaxError|LogicError|StyleError|OtherError>",
      "description": "<string>",
      "suggestion": "<string>"
    }}
  ],
  "fixed_code": "<string>",
  "summary": "<string>"
}}

Code to analyze:
{code}
"""

        # Get response from the model
        response = self.model.generate_code(prompt)

        # Clean the response to ensure it only contains the JSON part
        try:
            # Try to find JSON content between curly braces
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            if start_idx != -1 and end_idx != 0:
                json_str = response[start_idx:end_idx]
                debug_info = json.loads(json_str)
            else:
                raise json.JSONDecodeError("No JSON found", response, 0)

            # Validate the required fields
            required_fields = ['issues', 'fixed_code', 'summary']
            if not all(field in debug_info for field in required_fields):
                missing_fields = [field for field in required_fields if field not in debug_info]
                debug_info = {
                    "issues": [],
                    "fixed_code": "",
                    "summary": f"Invalid response format. Missing fields: {', '.join(missing_fields)}"
                }
            
            # Validate issues structure
            if 'issues' in debug_info:
                valid_issues = []
                for issue in debug_info['issues']:
                    if all(key in issue for key in ['line', 'type', 'description', 'suggestion']):
                        # Ensure line is an integer
                        issue['line'] = int(str(issue['line']).split('.')[0])
                        valid_issues.append(issue)
                debug_info['issues'] = valid_issues

        except (json.JSONDecodeError, ValueError) as e:
            debug_info = {
                "issues": [],
                "fixed_code": "",
                "summary": f"Model response parsing error: {str(e)}\nPlease try again with a different code snippet."
            }

        return debug_info