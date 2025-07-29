"""
finetuning: Modern fine-tuning library for LLMs
"""

__version__ = "0.1.0"

# Placeholder for main API
class FineTuner:
    """Main fine-tuning interface."""
    
    def __init__(self, model_name: str):
        self.model_name = model_name
        
    def train(self, dataset, method="lora", num_epochs=3):
        """Train the model."""
        raise NotImplementedError("Coming soon!")
        
    def save(self, path):
        """Save the fine-tuned model."""
        raise NotImplementedError("Coming soon!")

__all__ = ["FineTuner"]