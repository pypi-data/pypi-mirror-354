[![PyPI version](https://badge.fury.io/py/llm7-validator.svg)](https://badge.fury.io/py/llm7-validator)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://static.pepy.tech/badge/llm7-validator)](https://pepy.tech/project/llm7-validator)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-blue)](https://www.linkedin.com/in/eugene-evstafev-716669181/)

# llm7-validator

`llm7-validator` is a Python package designed to validate message structures sent to LLM7-compatible chat completion APIs. It ensures that model names, messages, and attachments conform to the expected structure and size constraints.

## Installation

To install `llm7-validator`, use pip:

```bash
pip install llm7-validator
````

## Usage

Here is a minimal example of how to use it:

```python
from llm7_validator import validate_chat_completion_request

check = validate_chat_completion_request({
    "model": "open-mistral-7b",
    "json_mode": True,
    "messages": [
        {"role": "system", "content": "hj"},
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What is this image?"},
                {"type": "image_url", "image_url": "https://example.com/image.png"},
            ],
        },
    ],
})

print(check)
```

## Features

* Verifies message format (`role`, `content`, etc.)
* Validates model names against a dynamically fetched list from [llm7-models.json](https://models.llm7.io/llm7-models.json)
* Checks:

  * Image URLs have allowed extensions (`.png`, `.jpg`, etc.)
  * Base64 image content length
  * Total request size (max 5 MB)
  * Required fields and optional tuning parameters
* Uses cached HTTP responses for model list with a 5-minute expiration

## Requirements

* `Python ≥ 3.10`
* `pydantic==2.11.5`
* `requests-cache==1.2.1`

## Contributing

Contributions, issues, and feature requests are welcome! Please visit the [GitHub repo](https://github.com/chigwell/llm7-validator/issues) to get started.

## License

`llm7-validator` is licensed under the [MIT License](https://opensource.org/licenses/MIT).
