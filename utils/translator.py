import os
import json
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class EnglishToArabicTranslator:
    """
    Senior NLP Translation Pipeline wrapping Hugging Face's Helsinki-NLP/opus-mt-en-ar model.
    Handles tokenization, sequence-to-sequence translation, device placement, and beam search decoding.
    """
    def __init__(self, model_name="Helsinki-NLP/opus-mt-en-ar", config_path=None):
        self.model_name = model_name
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = None
        self.model = None
        
        # Load custom config if provided
        self.config = {
            "default_max_length": 512,
            "default_num_beams": 4,
            "repetition_penalty": 1.2
        }
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    self.config.update(json.load(f))
            except Exception as e:
                print(f"[Warning] Failed to read config file {config_path}: {e}")

    def load_model(self):
        """Lazy load model and tokenizer onto target device."""
        if self.tokenizer is None or self.model is None:
            print(f"[NLP Engine] Loading translation model '{self.model_name}' on {self.device}...")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name).to(self.device)
            self.model.eval()
            print("[NLP Engine] Model and tokenizer loaded successfully!")
        return self.model, self.tokenizer

    def translate(self, text: str, max_length: int = None, num_beams: int = None) -> str:
        """
        Translates English text to Arabic.
        
        Args:
            text (str): Input English text string or multi-line paragraph.
            max_length (int): Maximum token sequence length for generation.
            num_beams (int): Number of beams for beam search decoding.
            
        Returns:
            str: Translated Arabic text string.
        """
        if not text or not text.strip():
            return ""

        self.load_model()
        
        max_length = max_length or self.config.get("default_max_length", 512)
        num_beams = num_beams or self.config.get("default_num_beams", 4)
        rep_penalty = self.config.get("repetition_penalty", 1.2)

        # Handle multi-line paragraphs cleanly
        paragraphs = text.split("\n")
        translated_paragraphs = []

        for paragraph in paragraphs:
            if not paragraph.strip():
                translated_paragraphs.append("")
                continue

            # Tokenize input sequence
            inputs = self.tokenizer(
                paragraph,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=max_length
            ).to(self.device)

            # Generate output sequence using beam search
            with torch.no_grad():
                generated_tokens = self.model.generate(
                    **inputs,
                    max_length=max_length,
                    num_beams=num_beams,
                    repetition_penalty=rep_penalty,
                    early_stopping=True
                )

            # Decode generated token IDs back to text string
            translated_text = self.tokenizer.decode(
                generated_tokens[0],
                skip_special_tokens=True
            )
            translated_paragraphs.append(translated_text)

        return "\n".join(translated_paragraphs)

    def get_token_count(self, text: str) -> int:
        """Helper to count token length for input text."""
        if not text:
            return 0
        self.load_model()
        tokens = self.tokenizer.encode(text)
        return len(tokens)
