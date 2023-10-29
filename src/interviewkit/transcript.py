import sys
from pathlib import Path

from rich.console import Console



from pydantic import BaseModel
from whisper.utils import get_writer


console = Console()


class Transcript(BaseModel):
    """The Transcript entity represents the transcript of an interview."""

    content: str


def transcribe_from_paths(source: Path, target: Path) -> None:
    console.print("Loading whisper base model...")
    model = whisper.load_model("base")

    with console.status("Transcribing audio file..."):
        result = model.transcribe((str(source)), fp16=False)

    # Setting some initial options values for the .txt output file
    txt_file_options = {
        "max_line_width": 50,
        "max_line_count": 1,
        "highlight_words": False,
    }

    # Save as a .txt file with hard breaks, added for readability to user
    console.print("Saving transcript as a .txt file...")
    txt_writer = get_writer("txt", str(target))
    txt_writer(result, source.name, txt_file_options)

    console.print("Transcript saved to:")
    console.print(f"    [green bold]{target / source.name}.txt[/green bold]")


if __name__ == "__main__":
    source = Path(sys.argv[1])
    target = Path(sys.argv[2])
    if source.suffix not in [".mp3", ".wav"]:
        raise ValueError("File must be an .mp3 or .wav file")
    transcribe_from_paths(source, target)
