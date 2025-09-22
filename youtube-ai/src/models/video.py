from pydantic import BaseModel, HttpUrl, Field
from typing import Optional, List

class VideoInfo(BaseModel):
    """Video metadata model"""
    url: HttpUrl
    title: Optional[str] = None
    duration: Optional[int] = None  # in seconds
    transcript_available: bool = False
    language: Optional[str] = None

class TranscriptSegment(BaseModel):
    """Single transcript segment with timestamp"""
    text: str
    start: float
    duration: float

class VideoTranscript(BaseModel):
    """Complete video transcript"""
    video_info: VideoInfo
    segments: List[TranscriptSegment]
    full_text: str = Field(default="")

    def model_post_init(self, __context) -> None:
        """Generate full text from segments"""
        if not self.full_text and self.segments:
            self.full_text = " ".join([segment.text for segment in self.segments])