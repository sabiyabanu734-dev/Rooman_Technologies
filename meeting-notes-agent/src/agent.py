import time
from pathlib import Path
from google import genai
from google.genai import types
from google.genai.errors import ServerError, APIError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from src.config import Config
from src.schemas import MeetingSummary


class MeetingNotesAgent:
    def __init__(self, model_name: str = Config.DEFAULT_MODEL):
        Config.validate()
        self.client = genai.Client(api_key=Config.GEMINI_API_KEY)
        self.model_name = model_name
        self.fallback_models = ["gemini-2.0-flash", "gemini-1.5-flash"]

    def process_file(self, file_path: str) -> MeetingSummary:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Transcript file not found at: {file_path}")

        raw_transcript = path.read_text(encoding="utf-8")
        return self.process_transcript(raw_transcript)

    @retry(
        stop=stop_after_attempt(4),
        wait=wait_exponential(multiplier=2, min=2, max=10),
        retry=retry_if_exception_type((ServerError, APIError)),
        reraise=True
    )
    def _execute_api_call(self, prompt: str, model_name: str):
        return self.client.models.generate_content(
            model=model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=MeetingSummary,
            ),
        )

    def process_transcript(self, transcript_text: str) -> MeetingSummary:
        prompt = (
            "You are an expert executive assistant. Analyze this meeting transcript to extract "
            "a structured summary, key decisions, and actionable tasks with assigned owners and realistic due dates.\n\n"
            f"Transcript:\n{transcript_text}"
        )

        models_to_try = [self.model_name] + [m for m in self.fallback_models if m != self.model_name]
        last_exception = None

        for model in models_to_try:
            try:
                response = self._execute_api_call(prompt, model)
                return MeetingSummary.model_validate_json(response.text)
            except Exception as e:
                last_exception = e
                continue

        raise last_exception