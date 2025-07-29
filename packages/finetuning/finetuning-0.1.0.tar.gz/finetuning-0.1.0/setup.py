"""
Setup configuration for finetuning package
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="finetuning",
    version="0.1.0",
    author="Synth AI",
    author_email="team@synth.ai",
    description="Modern fine-tuning library for LLMs with LoRA, QLoRA, and full fine-tuning support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/synth-ai/finetuning",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "torch>=2.0.0",
        "transformers>=4.35.0",
        "peft>=0.7.0",
        "accelerate>=0.25.0",
        "datasets>=2.14.0",
        "trl>=0.7.0",
    ],
    extras_require={
        "dev": ["pytest", "black", "flake8"],
        "modal": ["modal"],
    },
)