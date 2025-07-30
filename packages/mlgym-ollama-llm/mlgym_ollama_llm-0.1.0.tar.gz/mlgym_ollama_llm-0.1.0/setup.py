from setuptools import setup, find_packages

setup(
    name="mlgym_ollama_llm",
    version="0.1.0",
    description="A custom MLGym Ollama wrapper for LlamaIndex",
    author="Stratus5",
    author_email="operations@stratus5.com",
    packages=find_packages(),
    install_requires=[
        "llama-index>=0.12.0",
        "ollama>=0.5.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)