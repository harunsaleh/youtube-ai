from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field


class Quote(BaseModel):
    """Quote with timestamp"""

    text: str
    timestamp: str  # formatted as "MM:SS"


class MarkdownNote(BaseModel):
    """Generated markdown note structure"""

    title: str
    source_url: str
    tldr: Annotated[list[str], Field(min_length=3, max_length=5)]
    key_points: Annotated[list[str], Field(min_length=1)]
    outline: Annotated[list[str], Field(min_length=1)]
    quotes: list[Quote] = Field(default_factory=list)
    additional_sections: dict = Field(default_factory=dict)
    generated_at: datetime = Field(default_factory=datetime.now)

    def to_markdown(self) -> str:
        """Convert to markdown string"""
        md_content = f"# {self.title}\n\n"
        md_content += f"- Quelle: {self.source_url}\n\n"

        # TL;DR
        md_content += "## TL;DR\n\n"
        for point in self.tldr:
            md_content += f"- {point}\n"
        md_content += "\n"

        # Key Points
        md_content += "## Kernaussagen\n\n"
        for point in self.key_points:
            md_content += f"- {point}\n"
        md_content += "\n"

        # Outline
        md_content += "## Struktur / Outline\n\n"
        for i, item in enumerate(self.outline, 1):
            md_content += f"{i}. {item}\n"
        md_content += "\n"

        # Quotes if available
        if self.quotes:
            md_content += "## Wichtige Zitate\n\n"
            for quote in self.quotes:
                md_content += f'- "{quote.text}" ({quote.timestamp})\n'
            md_content += "\n"

        # Additional sections
        for section_name, content in self.additional_sections.items():
            md_content += f"## {section_name}\n\n"
            if isinstance(content, list):
                for item in content:
                    md_content += f"- {item}\n"
            else:
                md_content += f"{content}\n"
            md_content += "\n"

        return md_content
