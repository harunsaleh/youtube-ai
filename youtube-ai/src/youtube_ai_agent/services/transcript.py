from urllib.parse import parse_qs, urlparse

from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled

from pydantic import HttpUrl

from src.models.video import TranscriptSegment, VideoInfo, VideoTranscript


class TranscriptService:
    """Service for fetching YouTube transcripts"""

    def extract_video_id(self, url: str) -> str | None:
        """Extract video ID from YouTube URL"""
        parsed_url = urlparse(url)

        if parsed_url.hostname in ["www.youtube.com", "youtube.com"]:
            if parsed_url.path == "/watch":
                return parse_qs(parsed_url.query).get("v", [None])[0]
        elif parsed_url.hostname == "youtu.be":
            return parsed_url.path[1:]

        return None

    def fetch_transcript(self, url: str) -> VideoTranscript | None:
        """Fetch transcript for YouTube video"""
        video_id = self.extract_video_id(url)
        if not video_id:
            return None

        try:
            api = YouTubeTranscriptApi()
            transcript_list = api.list(video_id)

            try:
                transcript = transcript_list.find_transcript(["de"])
            except NoTranscriptFound:
                try:
                    transcript = transcript_list.find_transcript(["en"])
                except NoTranscriptFound:
                    transcript = transcript_list.find_generated_transcript(["de"])
                    if not transcript:
                        transcript = transcript_list.find_generated_transcript(["en"])

            if not transcript:
                return None

            transcript_data = transcript.fetch()

            segments = [
                TranscriptSegment(
                    text=entry.text, start=entry.start, duration=entry.duration
                )
                for entry in transcript_data
            ]

            video_info = VideoInfo(
                url=HttpUrl(url),
                transcript_available=True,
                language=getattr(transcript, "language_code", None),
            )

            return VideoTranscript(video_info=video_info, segments=segments)

        except (TranscriptsDisabled, NoTranscriptFound, Exception):
            return None

    def format_timestamp(self, seconds: float) -> str:
        """Convert seconds to MM:SS format"""
        minutes = int(seconds // 60)
        remaining_seconds = int(seconds % 60)
        return f"{minutes:02d}:{remaining_seconds:02d}"
