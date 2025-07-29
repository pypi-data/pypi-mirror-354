from setuptools import setup, find_packages

# Read requirements.txt
with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name="kalyan_ai",
    version="1.0.3",  # Incrementing version number
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
    install_requires=required,  # Using requirements from requirements.txt
    entry_points={
        "console_scripts": [
            "kalyan-ai=kalyan_ai:quick_setup",
            "kalyan-ai-server=kalyan_ai.api_server:main",
        ],
    },
    include_package_data=True,  # Include non-Python files specified in MANIFEST.in
    zip_safe=False,  # Ensure the package can be safely installed
)