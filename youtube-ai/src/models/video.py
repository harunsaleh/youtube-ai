from pydantic import BaseModel, Field, HttpUrl


class VideoInfo(BaseModel):
    """Video metadata model"""

    url: HttpUrl
    title: str | None = None
    duration: int | None = None  # in seconds
    transcript_available: bool = False
    language: str | None = None


class TranscriptSegment(BaseModel):
    """Single transcript segment with timestamp"""

    text: str
    start: float
    duration: float


class VideoTranscript(BaseModel):
    """Complete video transcript"""

    video_info: VideoInfo
    segments: list[TranscriptSegment]
    full_text: str = Field(default="")

    def model_post_init(self, __context) -> None:
        """Generate full text from segments"""
        if not self.full_text and self.segments:
            self.full_text = " ".join([segment.text for segment in self.segments])
