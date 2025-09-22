from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class Quote(BaseModel):
    """Quote with timestamp"""

    text: str
    timestamp: str  # formatted as "MM:SS"


class MarkdownNote(BaseModel):
    """Generated markdown note structure"""

    title: str
    source_url: str
    tldr: List[str] = Field(min_items=3, max_items=5)
    key_points: List[str] = Field(min_items=1)
    outline: List[str] = Field(min_items=1)
    quotes: List[Quote] = Field(default_factory=list)
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
