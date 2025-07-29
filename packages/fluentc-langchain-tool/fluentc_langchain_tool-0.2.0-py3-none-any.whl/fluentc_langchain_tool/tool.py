from langchain.tools import BaseTool
from typing import Type, Union, List
from .schemas import (
    TranslateInput, DetectLanguageInput, TranslationStatusInput, BatchTranslateInput,
    CheckLanguageInput, ResultsInput  # Legacy schemas
)
from .client import FluentCClient


class FluentCTranslationTool(BaseTool):
    name = "fluentc_translation"
    description = "Translate text using FluentC. Supports both real-time and batch translation modes."
    args_schema: Type = TranslateInput

    def __init__(self, api_key: str):
        super().__init__()
        self.client = FluentCClient(api_key)

    def _run(self, text: Union[str, List[str]], target_language: str, 
             source_language: str, mode: str = "realtime", 
             callback_url: str = None):
        try:
            result = self.client.translate(
                text=text,
                target_language=target_language,
                source_language=source_language,
                mode=mode,
                callback_url=callback_url
            )
            
            if mode == "realtime":
                if isinstance(text, list):
                    # Handle multiple translations
                    translations = result.get("translated_texts", [])
                    return f"Translations: {translations}"
                else:
                    return result.get("translated_text", "Translation failed.")
            else:  # batch mode
                job_id = result.get("job_id")
                status = result.get("status", "unknown")
                estimated_time = result.get("estimated_time_sec", "unknown")
                return f"Batch translation started. Job ID: {job_id}, Status: {status}, Estimated time: {estimated_time}s"
                
        except Exception as e:
            return f"Translation error: {str(e)}"


class FluentCBatchTranslationTool(BaseTool):
    name = "fluentc_batch_translation"
    description = "Translate text using FluentC batch mode with optional waiting for completion."
    args_schema: Type = BatchTranslateInput

    def __init__(self, api_key: str):
        super().__init__()
        self.client = FluentCClient(api_key)

    def _run(self, text: Union[str, List[str]], target_language: str,
             source_language: str, callback_url: str = None,
             wait_for_completion: bool = True, max_wait_time: int = 300):
        try:
            result = self.client.translate_batch(
                text=text,
                target_language=target_language,
                source_language=source_language,
                callback_url=callback_url,
                wait_for_completion=wait_for_completion,
                max_wait_time=max_wait_time
            )
            
            if wait_for_completion and result.get("status") == "complete":
                if isinstance(text, list):
                    translations = result.get("translated_texts", [])
                    return f"Batch translation completed. Translations: {translations}"
                else:
                    return f"Batch translation completed: {result.get('translated_text', '')}"
            else:
                job_id = result.get("job_id")
                status = result.get("status")
                return f"Batch translation job created. Job ID: {job_id}, Status: {status}"
                
        except Exception as e:
            return f"Batch translation error: {str(e)}"


class FluentCLanguageDetectorTool(BaseTool):
    name = "fluentc_language_detector"
    description = "Detect the language of text using FluentC."
    args_schema: Type = DetectLanguageInput

    def __init__(self, api_key: str):
        super().__init__()
        self.client = FluentCClient(api_key)

    def _run(self, text: str):
        try:
            result = self.client.detect_language(text)
            detected_lang = result.get("detected_language", "unknown")
            confidence = result.get("confidence", 0)
            return f"Detected language: {detected_lang} (confidence: {confidence:.2f})"
        except Exception as e:
            return f"Language detection error: {str(e)}"


class FluentCTranslationStatusTool(BaseTool):
    name = "fluentc_translation_status"
    description = "Check the status of a batch translation job using job ID."
    args_schema: Type = TranslationStatusInput

    def __init__(self, api_key: str):
        super().__init__()
        self.client = FluentCClient(api_key)

    def _run(self, job_id: str):
        try:
            result = self.client.get_translation_status(job_id)
            status = result.get("status", "unknown")
            
            if status == "complete":
                translated_text = result.get("translated_text", "")
                source_lang = result.get("source_language", "unknown")
                target_lang = result.get("target_language", "unknown")
                processing_time = result.get("meta", {}).get("processing_time_ms", "unknown")
                return f"Translation complete: {translated_text}\nSource: {source_lang} -> Target: {target_lang}\nProcessing time: {processing_time}ms"
            elif status in ["queued", "processing"]:
                estimated_time = result.get("estimated_time_sec", 5)
                return f"Status: {status}. Estimated remaining time: {estimated_time} seconds."
            elif status == "failed":
                error = result.get("error", "Unknown error")
                return f"Translation failed: {error}"
            else:
                return f"Status: {status}"
                
        except Exception as e:
            return f"Status check error: {str(e)}"


class FluentCSupportedLanguagesTool(BaseTool):
    name = "fluentc_supported_languages"
    description = "Get list of supported languages from FluentC."
    args_schema: Type = None

    def __init__(self, api_key: str):
        super().__init__()
        self.client = FluentCClient(api_key)

    def _run(self):
        try:
            result = self.client.get_supported_languages()
            source_langs = result.get("source_languages", [])
            target_langs = result.get("target_languages", [])
            
            return f"Supported source languages: {', '.join(source_langs)}\nSupported target languages: {', '.join(target_langs)}"
        except Exception as e:
            return f"Error getting supported languages: {str(e)}"


# Legacy tools for backward compatibility
class FluentCResultsTool(BaseTool):
    name = "fluentc_results"
    description = "Poll the result of a batch translation using job_id (legacy - use fluentc_translation_status instead)."
    args_schema: Type = ResultsInput

    def __init__(self, api_key: str):
        super().__init__()
        self.client = FluentCClient(api_key)

    def _run(self, job_id):
        try:
            result = self.client.get_results(job_id)  # Uses legacy method internally
            if result["status"] == "complete":
                return result.get("translated_text", result.get("translation", ""))
            elif result["status"] in ["queued", "processing"]:
                wait_time = result.get("estimated_time_sec", result.get("estimated_wait_seconds", 5))
                return f"Still processing. Try again in {wait_time} seconds."
            elif result["status"] == "failed":
                return f"Translation failed: {result.get('error')}"
            return f"Unknown status: {result['status']}"
        except Exception as e:
            return f"Error getting results: {str(e)}"
