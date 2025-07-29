from setuptools import setup, find_packages

setup(
    name="claude-sdk",
    version="0.0.1",
    author="Anthropic",
    author_email="support@anthropic.com",
    description="A placeholder for the Claude SDK Python package",
    long_description="This is a placeholder package for the Claude SDK. The official SDK is coming soon.",
    long_description_content_type="text/plain",
    url="https://github.com/Anthropic/python-sdk",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
)