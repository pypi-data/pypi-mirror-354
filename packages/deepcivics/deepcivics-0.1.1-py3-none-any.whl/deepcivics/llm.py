# LLM wrapper
from transformers import pipeline
from deepcivics.models import get_model_name

class CivicLLM:
    def __init__(self, model_name="multilingual_default", device="cpu"):
        """
        Initialize the question-answering pipeline using a model alias or full name.

        Args:
            model_name (str): Model alias (e.g. 'english_default') or full HF model name
            device (str): 'cpu' or 'cuda' (default: 'cpu')
        """
        resolved_name = get_model_name(model_name)
        try:
            self.qa = pipeline("question-answering", model=resolved_name, device=0 if device == "cuda" else -1)
        except Exception as e:
            raise RuntimeError(f"❌ Failed to load model '{resolved_name}': {e}")

    def ask(self, question: str, context: str) -> str:
        """
        Ask a question given the context (must be text).

        Args:
            question (str): Natural language question
            context (str): A string containing data context (e.g. CSV text)

        Returns:
            str: Answer from the model
        """
        result = self.qa({
            "question": question,
            "context": context
        })
        return result["answer"]
