import os
from pathlib import Path

import click
from slugify import slugify

from src.youtube_ai_agent.config import settings
from src.youtube_ai_agent.services.ai_service import AIService
from src.youtube_ai_agent.services.transcript import TranscriptService


@click.command()
@click.argument("youtube_url")
@click.option(
    "--output-dir", "-o", default=None, help="Output directory for markdown files"
)
@click.option("--model", "-m", default=None, help="AI model to use")
@click.option("--verbose", "-v", is_flag=True, help="Verbose output")
def process_video(
    youtube_url: str, output_dir: str | None, model: str | None, verbose: bool
):
    """Process YouTube video and generate structured markdown notes."""

    # Override settings if provided
    if output_dir:
        settings.output_dir = output_dir
    if model:
        settings.ai_model = model

    # Ensure output directory exists
    output_path = Path(settings.output_dir)
    output_path.mkdir(exist_ok=True)

    if verbose:
        click.echo(f"Processing: {youtube_url}")
        click.echo(f"Output directory: {output_path.absolute()}")
        click.echo(f"Using model: {settings.ai_model}")

    # Initialize services
    transcript_service = TranscriptService()
    ai_service = AIService()

    try:
        # Step 1: Fetch transcript
        if verbose:
            click.echo("Fetching transcript...")

        video_transcript = transcript_service.fetch_transcript(youtube_url)
        if not video_transcript:
            click.echo(
                "[ERROR] Could not fetch transcript. Please try another video.",
                err=True,
            )
            return

        if verbose:
            click.echo(
                f"[SUCCESS] Transcript fetched "
                f"({len(video_transcript.segments)} segments)"
            )

        # Step 2: Generate markdown note
        if verbose:
            click.echo("Generating structured notes...")

        markdown_note = ai_service.generate_note(video_transcript)
        if not markdown_note:
            click.echo("[ERROR] Could not generate notes from transcript.", err=True)
            return

        # Step 3: Save to file
        slug = slugify(markdown_note.title)[:50]  # Limit filename length
        output_file = output_path / f"{slug}.md"

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(markdown_note.to_markdown())

        click.echo(f"[SUCCESS] Generated notes saved to: {output_file}")

        if verbose:
            click.echo(f"Title: {markdown_note.title}")
            click.echo(f"TL;DR points: {len(markdown_note.tldr)}")
            click.echo(f"Key points: {len(markdown_note.key_points)}")
            click.echo(f"Outline items: {len(markdown_note.outline)}")

    except Exception as e:
        click.echo(f"[ERROR] Error processing video: {str(e)}", err=True)
        if verbose:
            import traceback

            click.echo(traceback.format_exc(), err=True)


@click.group()
def cli():
    """YouTube AI Agent - Convert YouTube videos to structured markdown notes."""
    pass


@cli.command()
def setup():
    """Setup configuration and check API keys."""
    click.echo("YouTube AI Agent Setup")
    click.echo("=" * 50)

    # Check API keys
    if settings.openai_api_key:
        click.echo("[OK] OpenAI API key found")
    else:
        click.echo("[MISSING] OpenAI API key not found (set OPENAI_API_KEY)")

    click.echo(f"Current AI provider: {settings.ai_provider}")
    click.echo(f"Current model: {settings.ai_model}")
    click.echo(f"Output directory: {settings.output_dir}")

    # Create .env template if it doesn't exist
    if not os.path.exists(".env"):
        with open(".env.example", "w") as f:
            f.write("""# AI Provider Configuration
OPENAI_API_KEY=your_openai_api_key_here
AI_PROVIDER=openai
AI_MODEL=gpt-4o-mini

# Output Configuration
OUTPUT_DIR=output

# Processing Configuration
MAX_TRANSCRIPT_LENGTH=10000
""")
        click.echo("Created .env.example - copy to .env and fill in your API keys")


cli.add_command(process_video)

if __name__ == "__main__":
    cli()
