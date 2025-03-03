from app.models.code_model import QwenCoderModel
import json

class Suggestion:
    def __init__(self):
        self.model = QwenCoderModel()

    def get_suggestion(self, analysis, debuging ) -> str:
        prompt = f"""You are a knowledgeable code mentor bot. Your task is to analyze the provided code analysis and debugging report and offer concise, actionable suggestions.

        Analysis: {analysis}  
        Debugging Report: {debuging}  

        Your response should be under 100 words and follow this format:  
        - **Optimization Suggestions**: [If any, suggest improvements for performance, readability, or efficiency]  
        - **Bug Fixes**: [Identify and suggest fixes for errors or logical issues]  

        Keep the suggestions clear and to the point.
        """
        

        response = self.model.generate_code(prompt)
        
        return response.content