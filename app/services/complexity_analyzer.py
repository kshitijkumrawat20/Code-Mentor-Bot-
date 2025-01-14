from app.models.code_model import QwenCoderModel
import json

class ComplexityAnalyzer:
    def __init__(self):
        self.model = QwenCoderModel()

    def analyze_complexity(self, code: str) -> dict:
        prompt = f"""You are a helpful code mentor bot. Analyze the space and time complexity of the given code.
Respond with ONLY a JSON object in the exact format shown below, with no additional text:

{{
    "time_complexity": {{
        "overall": "<string: Big O notation>",
        "explanation": "<string>",
        "breakdown": [
            {{
                "section": "<string: function or block name>",
                "complexity": "<string: Big O notation>",
                "explanation": "<string>"
            }}
        ]
    }},
    "space_complexity": {{
        "overall": "<string: Big O notation>",
        "explanation": "<string>"
    }},
    "optimization_suggestions": [
        {{
            "description": "<string>",
            "impact": "<string: Expected improvement>"
        }}
    ],
    "summary": "<string: Brief overview>"
}}

Code to analyze:
{code}
"""

        response = self.model.generate_code(prompt)

        try:
            # Try to find JSON content between curly braces
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            if start_idx != -1 and end_idx != 0:
                json_str = response[start_idx:end_idx]
                result = json.loads(json_str)
            else:
                raise json.JSONDecodeError("No JSON found", response, 0)

            # Validate the required fields
            required_fields = ['time_complexity', 'space_complexity', 'optimization_suggestions', 'summary']
            if not all(field in result for field in required_fields):
                missing_fields = [field for field in required_fields if field not in result]
                result = {
                    "time_complexity": {"overall": "N/A", "explanation": "Analysis failed", "breakdown": []},
                    "space_complexity": {"overall": "N/A", "explanation": "Analysis failed"},
                    "optimization_suggestions": [],
                    "summary": f"Invalid response format. Missing fields: {', '.join(missing_fields)}"
                }

        except json.JSONDecodeError as e:
            result = {
                "time_complexity": {"overall": "N/A", "explanation": "Analysis failed", "breakdown": []},
                "space_complexity": {"overall": "N/A", "explanation": "Analysis failed"},
                "optimization_suggestions": [],
                "summary": f"Failed to parse the model response: {str(e)}"
            }

        return result