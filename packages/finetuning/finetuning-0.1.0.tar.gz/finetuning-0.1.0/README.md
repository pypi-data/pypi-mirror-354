# finetuning

Modern fine-tuning library for Large Language Models (LLMs) with support for LoRA, QLoRA, and full fine-tuning.

## Features

- 🚀 Easy-to-use API for fine-tuning LLMs
- 🔧 Support for LoRA and QLoRA parameter-efficient methods  
- 📊 Built-in evaluation and metrics
- ☁️ Cloud-native with Modal integration
- 🔄 Compatible with HuggingFace models

## Installation

```bash
pip install finetuning
```

## Quick Start

```python
from finetuning import FineTuner

# Initialize fine-tuner
tuner = FineTuner(model_name="meta-llama/Llama-2-7b-hf")

# Fine-tune on your data
tuner.train(
    dataset="your_dataset",
    method="lora",  # or "qlora", "full"
    num_epochs=3
)

# Save fine-tuned model
tuner.save("./my_finetuned_model")
```

## License

MIT