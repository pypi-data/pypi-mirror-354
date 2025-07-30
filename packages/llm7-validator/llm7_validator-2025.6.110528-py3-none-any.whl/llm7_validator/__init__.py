import json
import threading
from datetime import timedelta
from requests_cache import CachedSession
from typing import List, Union, Literal, Optional, Annotated
from pydantic import (
    BaseModel,
    HttpUrl,
    field_validator,
    constr,
    conlist,
    confloat,
    conint,
    StringConstraints,
    ValidationError,
)


_model_lock = threading.Lock()
_cached_models: Optional[List[str]] = None
_last_fetch: Optional[float] = None
_MODEL_CACHE_SECONDS = 300
_MODEL_ENDPOINT = "https://models.llm7.io/llm7-models.json"
session = CachedSession(
    "llm7_model_cache", expire_after=timedelta(seconds=_MODEL_CACHE_SECONDS)
)

Base64ImageStr = Annotated[
    str, StringConstraints(pattern=r"^data:image\/.*;base64,.+$", max_length=1_000_000)
]


def get_valid_model_ids() -> List[str]:
    """
    Fetches the list of valid model IDs from the LLM7 models endpoint.
    If the cached models are available and not expired, it returns them.

    :return:
        List of valid model IDs.
    """
    global _cached_models, _last_fetch
    with _model_lock:
        if _cached_models is not None:
            return _cached_models

        response = session.get(_MODEL_ENDPOINT)
        response.raise_for_status()
        _cached_models = [entry["id"] for entry in response.json().get("chat", [])]
        return _cached_models


class ImageUrl(BaseModel):
    type: Literal["image_url"]
    image_url: HttpUrl

    @field_validator("image_url")
    @classmethod
    def url_must_end_with_image_extension(cls, v: HttpUrl) -> HttpUrl:
        valid_extensions = (".png", ".jpg", ".jpeg", ".webp")
        if not str(v).lower().endswith(valid_extensions):
            raise ValueError(f"Image URL must end with one of {valid_extensions}")
        return v


class ImageBase64(BaseModel):
    type: Literal["image_url"]
    image_url: Base64ImageStr


class TextContent(BaseModel):
    type: Literal["text"]
    text: constr(min_length=1, max_length=10_000)


Content = Union[TextContent, ImageUrl, ImageBase64]


class Message(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: Union[constr(min_length=1, max_length=10_000), List[Content]]

    @field_validator("content")
    @classmethod
    def system_message_must_be_str(cls, v, info):
        role = info.data["role"]
        if role == "system" and not isinstance(v, str):
            raise ValueError("System messages must have string content.")
        return v


class ChatCompletionRequest(BaseModel):
    model: str
    messages: conlist(Message, min_length=1, max_length=50)
    seed: Optional[conint(ge=0)] = None
    temperature: Optional[confloat(ge=0.0, le=3.0)] = 1.0
    top_p: Optional[confloat(ge=0.0, le=1.0)] = 1.0
    presence_penalty: Optional[confloat(ge=-2.0, le=2.0)] = 0.0
    frequency_penalty: Optional[confloat(ge=-2.0, le=2.0)] = 0.0
    json_mode: Optional[bool] = False
    stream: bool = False
    retry: bool = False

    @field_validator("messages")
    @classmethod
    def total_request_size_limit(cls, v: List[Message]) -> List[Message]:
        total_size_kb = (
            len(
                json.dumps([message.model_dump(mode="json") for message in v]).encode(
                    "utf-8"
                )
            )
            / 1024
            / 1024
        )

        if total_size_kb > 5:  # 5 MB limit
            raise ValueError("Total request size cannot exceed 5 MB.")
        return v

    @field_validator("model")
    @classmethod
    def validate_model(cls, v: str) -> str:
        valid_ids = get_valid_model_ids()
        if v not in valid_ids:
            raise ValueError(
                f"Invalid model '{v}'. Must be one of: {', '.join(valid_ids)}"
            )
        return v


def validate_chat_completion_request(data: dict) -> ChatCompletionRequest:
    """
    Validates the provided data against the ChatCompletionRequest model.
    :param data:
        Dictionary containing the request data to validate.
    :return:
        A dictionary with validation results:
        - "valid": True if the data is valid, False otherwise.
        - "message": A message indicating the result of the validation.
        - "errors": List of validation errors if any.
        - "data": The original data that was validated.
    """
    try:
        ChatCompletionRequest(**data)
        return {
            "valid": True,
            "message": "Request is valid.",
            "errors": [],
            "data": data,
        }
    except ValidationError as e:
        return {
            "valid": False,
            "message": "Validation error",
            "errors": e.errors(),
            "data": data,
        }
