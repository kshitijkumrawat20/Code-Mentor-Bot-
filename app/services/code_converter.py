from app.models.code_model import QwenCoderModel

class CodeConverter:
    def __init__(self):
        self.model = QwenCoderModel()  # Initialize the Qwen model

    def convert_code(self, code: str, source_lang: str, target_lang: str) -> str:
        # Create a prompt for the model to convert the code from source_lang to target_lang
        prompt = f"""You are a helpful code mentor bot. Your task is to convert code from one programming language to another.
Convert the following {source_lang} code to {target_lang}:

{code}
"""

        # Use the model to generate a response based on the prompt
        converted_code = self.model.generate_code(prompt)

        return converted_code
