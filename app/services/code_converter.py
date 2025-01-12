from transformers import T5ForConditionalGeneration, AutoTokenizer
import torch
from typing import Dict, Optional

class CodeConverter:
    def __init__(self):
        self.checkpoint = "Salesforce/codet5p-770m"
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = AutoTokenizer.from_pretrained(self.checkpoint)
        self.model = T5ForConditionalGeneration.from_pretrained(self.checkpoint).to(self.device)

    def convert_code(self, code: str, source_lang: str, target_lang: str) -> Dict:
        try:
            # Create a more specific prompt
            prompt = f"""
Translate this {source_lang} code to {target_lang}:

{code}

Converted {target_lang} code:
"""
            # Generate the conversion
            inputs = self.tokenizer.encode(prompt, return_tensors="pt").to(self.device)
            outputs = self.model.generate(
                inputs,
                max_length=512,
                num_return_sequences=1,
                temperature=0.2,  # Reduced temperature for more deterministic output
                top_p=0.95,
                do_sample=False,  # Disable sampling for more consistent results
                num_beams=5  # Use beam search for better quality
            )
            
            converted_code = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Clean up the converted code
            converted_code = self._clean_converted_code(converted_code, target_lang)
            
            return {
                "converted_code": converted_code,
                "source_lang": source_lang,
                "target_lang": target_lang
            }
            
        except Exception as e:
            return {
                "error": f"Conversion failed: {str(e)}",
                "source_lang": source_lang,
                "target_lang": target_lang
            }

    def _clean_converted_code(self, code: str, target_lang: str) -> str:
        # Remove any generated markers or artifacts
        code = code.replace("Converted code:", "").strip()
        code = code.replace("```javascript", "").replace("```", "").strip()
        
        # Apply language-specific formatting
        if target_lang == "javascript":
            # Ensure proper JavaScript formatting
            lines = code.split('\n')
            cleaned_lines = []
            for line in lines:
                line = line.strip()
                if line and not line.startswith(('/', '#')):  # Skip comment lines
                    # Add semicolons if needed
                    if not line.endswith('{') and not line.endswith('}') and not line.endswith(';'):
                        line += ';'
                    cleaned_lines.append(line)
            
            # Join lines and format
            code = '\n'.join(cleaned_lines)
            
            # Ensure function declaration is correct
            code = code.replace("def ", "function ")
            
        return code

    def get_language_template(self, target_lang: str) -> Dict:
        templates = {
            "javascript": {
                "function": "function name(params) {\n    // code\n}",
                "if": "if (condition) {\n    // code\n}",
                "for": "for (let i = 0; i < n; i++) {\n    // code\n}",
                "while": "while (condition) {\n    // code\n}"
            },
            "python": {
                "function": "def name(params):\n    # code",
                "if": "if condition:\n    # code",
                "for": "for i in range(n):\n    # code",
                "while": "while condition:\n    # code"
            }
        }
        return templates.get(target_lang, {}) 