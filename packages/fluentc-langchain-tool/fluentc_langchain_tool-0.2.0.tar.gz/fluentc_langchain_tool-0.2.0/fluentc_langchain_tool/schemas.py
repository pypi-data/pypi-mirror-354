from pydantic import BaseModel
from typing import Optional, Union, List


class TranslateInput(BaseModel):
    text: Union[str, List[str]]
    target_language: str
    source_language: str
    mode: str = "realtime"
    callback_url: Optional[str] = None


class DetectLanguageInput(BaseModel):
    text: str


class TranslationStatusInput(BaseModel):
    job_id: str


class BatchTranslateInput(BaseModel):
    text: Union[str, List[str]]
    target_language: str
    source_language: str
    callback_url: Optional[str] = None
    wait_for_completion: bool = True
    max_wait_time: int = 300


# Legacy schemas for backward compatibility
class CheckLanguageInput(BaseModel):
    input: str
    input_format: str


class ResultsInput(BaseModel):
    job_id: str
