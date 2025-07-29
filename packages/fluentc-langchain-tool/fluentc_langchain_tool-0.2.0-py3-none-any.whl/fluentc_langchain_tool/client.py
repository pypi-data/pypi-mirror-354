import requests
from typing import Optional, Union, Dict, Any
import time


class FluentCClient:
    def __init__(self, api_key: str, api_base: str = "https://api.fluentc.ai"):
        self.api_key = api_key
        self.api_base = api_base

    def _headers(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self.api_key}"}

    def translate(
        self, 
        text: Union[str, list], 
        target_language: str, 
        source_language: str,
        mode: str = "realtime",
        callback_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Translate text using FluentC API.
        
        Args:
            text: Text to translate (string or list of strings)
            target_language: Target language code (e.g., 'fr', 'es', 'de')
            source_language: Source language code (required)
            mode: Translation mode - 'realtime' or 'batch' (default: 'realtime')
            callback_url: Optional callback URL for batch mode notifications
            
        Returns:
            Dictionary containing translation result or job information
        """
        data = {
            "text": text,
            "target_language": target_language,
            "source_language": source_language,
            "mode": mode
        }
            
        if callback_url:
            data["callback_url"] = callback_url
            
        res = requests.post(f"{self.api_base}/translate", json=data, headers=self._headers())
        res.raise_for_status()
        return res.json()

    def get_translation_status(self, job_id: str) -> Dict[str, Any]:
        """
        Get the status of a batch translation job.
        
        Args:
            job_id: The job ID returned from a batch translation request
            
        Returns:
            Dictionary containing job status and results (if complete)
        """
        res = requests.get(f"{self.api_base}/translate/status", 
                          params={"job_id": job_id}, 
                          headers=self._headers())
        res.raise_for_status()
        return res.json()

    def wait_for_translation(self, job_id: str, max_wait_time: int = 300, poll_interval: int = 2) -> Dict[str, Any]:
        """
        Wait for a batch translation to complete by polling the status.
        
        Args:
            job_id: The job ID returned from a batch translation request
            max_wait_time: Maximum time to wait in seconds (default: 300)
            poll_interval: Time between status checks in seconds (default: 2)
            
        Returns:
            Dictionary containing final translation results
            
        Raises:
            TimeoutError: If translation doesn't complete within max_wait_time
            RuntimeError: If translation fails
        """
        start_time = time.time()
        
        while time.time() - start_time < max_wait_time:
            status = self.get_translation_status(job_id)
            
            if status.get("status") == "complete":
                return status
            elif status.get("status") == "failed":
                raise RuntimeError(f"Translation failed: {status.get('error', 'Unknown error')}")
            
            time.sleep(poll_interval)
        
        raise TimeoutError(f"Translation did not complete within {max_wait_time} seconds")

    def translate_batch(
        self, 
        text: Union[str, list], 
        target_language: str, 
        source_language: str,
        callback_url: Optional[str] = None,
        wait_for_completion: bool = True,
        max_wait_time: int = 300
    ) -> Dict[str, Any]:
        """
        Convenience method for batch translation with optional waiting.
        
        Args:
            text: Text to translate (string or list of strings)
            target_language: Target language code
            source_language: Source language code (required)
            callback_url: Optional callback URL for notifications
            wait_for_completion: Whether to wait for completion (default: True)
            max_wait_time: Maximum time to wait if waiting for completion
            
        Returns:
            Translation results if wait_for_completion=True, otherwise job info
        """
        result = self.translate(
            text=text, 
            target_language=target_language, 
            source_language=source_language,
            mode="batch",
            callback_url=callback_url
        )
        
        if wait_for_completion and "job_id" in result:
            return self.wait_for_translation(result["job_id"], max_wait_time)
        
        return result

    def get_supported_languages(self) -> Dict[str, Any]:
        """
        Get list of supported languages.
        
        Returns:
            Dictionary containing supported source and target languages
        """
        res = requests.get(f"{self.api_base}/languages", headers=self._headers())
        res.raise_for_status()
        return res.json()

    def detect_language(self, text: str) -> Dict[str, Any]:
        """
        Detect the language of given text.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary containing detected language information
        """
        data = {"text": text}
        res = requests.post(f"{self.api_base}/detect", json=data, headers=self._headers())
        res.raise_for_status()
        return res.json()

    # Legacy methods for backward compatibility
    def languages(self, data: dict) -> dict:
        """Legacy method - use get_supported_languages() instead."""
        return self.get_supported_languages()

    def check_language(self, data: dict) -> dict:
        """Legacy method - use detect_language() instead."""
        if "text" in data:
            return self.detect_language(data["text"])
        raise ValueError("Missing 'text' field in data")

    def get_results(self, job_id: str) -> dict:
        """Legacy method - use get_translation_status() instead."""
        return self.get_translation_status(job_id)
