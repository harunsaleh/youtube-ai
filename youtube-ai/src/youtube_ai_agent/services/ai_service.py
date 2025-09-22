from typing import Optional
import json
import re
from openai import OpenAI

from src.models.video import VideoTranscript
from src.models.note import MarkdownNote, Quote
from ..config import settings


class AIService:
    """Service for AI-powered content analysis"""

    def __init__(self):
        if settings.ai_provider == "openai" and settings.openai_api_key:
            self.client = OpenAI(api_key=settings.openai_api_key)
        else:
            raise ValueError("OpenAI API key not configured")

    def generate_note(
        self, video_transcript: VideoTranscript
    ) -> Optional[MarkdownNote]:
        """Generate structured markdown note from video transcript"""

        # Truncate transcript if too long
        transcript_text = video_transcript.full_text
        if len(transcript_text) > settings.max_transcript_length:
            transcript_text = transcript_text[: settings.max_transcript_length] + "..."

        prompt = self._build_prompt(video_transcript.video_info.url, transcript_text)

        try:
            response = self.client.chat.completions.create(
                model=settings.ai_model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
                max_tokens=2000,
            )

            content = response.choices[0].message.content
            return self._parse_ai_response(
                content, str(video_transcript.video_info.url)
            )

        except Exception as e:
            print(f"Error calling AI service: {e}")
            return None

    def _get_system_prompt(self) -> str:
        """Get system prompt for AI model"""
        return """Du bist ein AI-Agent, der YouTube-Video-Transkripte analysiert und strukturierte Notizen erstellt.

Deine Aufgabe:
- Analysiere das bereitgestellte Transkript gründlich
- Extrahiere die wichtigsten Inhalte 
- Erstelle eine klar strukturierte Zusammenfassung

Antworte ausschließlich im folgenden JSON-Format:
{
  "title": "Aussagekräftiger Titel des Videos/Themas",
  "tldr": ["Punkt 1", "Punkt 2", "Punkt 3"],
  "key_points": ["Kernaussage 1", "Kernaussage 2", "..."],
  "outline": ["Gliederungspunkt 1", "Gliederungspunkt 2", "..."],
  "quotes": [{"text": "Wichtiges Zitat", "timestamp": "MM:SS"}],
  "additional_sections": {
    "Offene Fragen": ["Frage 1", "Frage 2"],
    "Glossar": ["Begriff: Erklärung"]
  }
}

Wichtig:
- TL;DR: 3-5 prägnante Bullet Points
- Kernaussagen: Die wichtigsten Erkenntnisse
- Outline: Logische Struktur des Inhalts
- Zeitstempel nur bei verfügbaren Informationen
- Zusatzsektionen sind optional aber erwünscht"""

    def _build_prompt(self, video_url: str, transcript: str) -> str:
        """Build prompt for AI model"""
        return f"""Analysiere bitte das folgende YouTube-Video-Transkript und erstelle strukturierte Notizen:

Video-URL: {video_url}

Transkript:
{transcript}

Erstelle eine strukturierte Analyse mit den wichtigsten Inhalten, Kernaussagen und einer logischen Gliederung."""

    def _parse_ai_response(
        self, content: str, source_url: str
    ) -> Optional[MarkdownNote]:
        """Parse AI response and create MarkdownNote"""
        try:
            # Extract JSON from response (in case there's extra text)
            json_match = re.search(r"\{.*\}", content, re.DOTALL)
            if json_match:
                json_str = json_match.group()
            else:
                json_str = content

            data = json.loads(json_str)

            # Parse quotes if present
            quotes = []
            if "quotes" in data and data["quotes"]:
                for quote_data in data["quotes"]:
                    if isinstance(quote_data, dict) and "text" in quote_data:
                        quotes.append(
                            Quote(
                                text=quote_data["text"],
                                timestamp=quote_data.get("timestamp", "00:00"),
                            )
                        )

            return MarkdownNote(
                title=data.get("title", "Untitled"),
                source_url=source_url,
                tldr=data.get("tldr", []),
                key_points=data.get("key_points", []),
                outline=data.get("outline", []),
                quotes=quotes,
                additional_sections=data.get("additional_sections", {}),
            )

        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"Error parsing AI response: {e}")
            print(f"Raw response: {content}")
            return None