from setuptools import setup, find_packages

setup(
    name="kalyan_ai",  # Changed to unique name
    version="1.0.2",  # Incrementing version number
    author="Kalyan",
    author_email="your.email@example.com",
    description="Local AI assistant with Ollama integration - OpenAI compatible API",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/kalyan-ai",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "fastapi>=0.68.0",
        "uvicorn>=0.15.0",
        "requests>=2.25.1",
        "pydantic>=1.8.0",
        "python-multipart>=0.0.5",
    ],
    entry_points={
        "console_scripts": [
            "kalyan-ai=kalyan_ai:quick_setup",
            "kalyan-ai-server=kalyan_ai.api_server:main",
        ],
    },
)