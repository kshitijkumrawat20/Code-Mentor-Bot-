#code_model.py
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class QwenCoderModel:
    def __init__(self):
        self.model_name = "Qwen/Qwen2.5-Coder-0.5B-Instruct"
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype="auto",
            device_map="auto"
        ).to(self.device)

    def generate_code(self, prompt: str, max_length: int = 512) -> str:
        messages = [
            {"role": "system", "content": "You are a helpful code assistant."},
            {"role": "user", "content": prompt}
        ]
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.device)
        generated_ids = self.model.generate(
            **model_inputs,
            max_new_tokens=max_length
        )
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]
        return self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

    def debug_code(self, code: str) -> str:
        prompt = f"Debug this code: {code}"
        return self.generate_code(prompt)

    def convert_code(self, code: str, source_lang: str, target_lang: str) -> str:
        prompt = f"Convert this {source_lang} code to {target_lang}: {code}"
        return self.generate_code(prompt)

