from transformers import T5ForConditionalGeneration, AutoTokenizer
import torch

class CodeT5Model:
    def __init__(self):
        self.checkpoint = "Salesforce/codet5p-770m"
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = AutoTokenizer.from_pretrained(self.checkpoint)
        self.model = T5ForConditionalGeneration.from_pretrained(self.checkpoint).to(self.device)

    def generate_code(self, prompt: str, max_length: int = 512) -> str:
        inputs = self.tokenizer.encode(prompt, return_tensors="pt").to(self.device)
        outputs = self.model.generate(inputs, max_length=max_length)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)

    def debug_code(self, code: str) -> str:
        prompt = f"Debug this code: {code}"
        return self.generate_code(prompt)

    def convert_code(self, code: str, source_lang: str, target_lang: str) -> str:
        prompt = f"Convert this {source_lang} code to {target_lang}: {code}"
        return self.generate_code(prompt) 