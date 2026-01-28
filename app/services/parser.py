from pathlib import Path
from typing import Iterable

from docling.document_converter import DocumentConverter


class DocumentParser:
    def __init__(self) -> None:
        self._converter = DocumentConverter()

    def parse(self, source: Path) -> str:
        result = self._converter.convert(str(source))
        return result.document.export_to_markdown()


def cleanup_files(paths: Iterable[Path]) -> None:
    for path in paths:
        try:
            path.unlink(missing_ok=True)
        except OSError:
            # Best-effort cleanup; log at call site if needed.
            pass
