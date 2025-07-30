from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="llm7-validator",
    version="2025.6.110528",
    author="Eugene Evstafev",
    author_email="support@llm7.io",
    description="Validator for LLM7 chat completion requests with Pydantic and model ID constraints.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chigwell/llm7-validator",
    packages=find_packages(),
    install_requires=["requests-cache==1.2.1", "pydantic==2.11.5", "typing==3.7.4.3"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    license="MIT",
    tests_require=["unittest"],
    test_suite="test",
)
