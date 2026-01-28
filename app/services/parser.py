from pathlib import Path
from typing import Iterable

from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import AcceleratorOptions, PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption

from app.core.config import settings


class DocumentParser:
    def __init__(self) -> None:
        pipeline_options = PdfPipelineOptions(
            do_ocr=False,
            do_table_structure=True,
            do_picture_classification=False,
            do_picture_description=False,
            do_code_enrichment=False,
            do_formula_enrichment=False,
            generate_page_images=False,
            generate_picture_images=False,
            generate_table_images=False,
            generate_parsed_pages=False,
            document_timeout=settings.docling_timeout_s,
            accelerator_options=AcceleratorOptions(
                num_threads=settings.docling_num_threads,
                device=settings.docling_device,
            ),
        )
        format_options = {
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }
        self._converter = DocumentConverter(format_options=format_options)

    def parse(self, source: Path) -> str:
        result = self._converter.convert(
            str(source),
            max_num_pages=settings.docling_max_num_pages,
            max_file_size=settings.docling_max_file_size_mb * 1024 * 1024,
        )
        return result.document.export_to_markdown()


def cleanup_files(paths: Iterable[Path]) -> None:
    for path in paths:
        try:
            path.unlink(missing_ok=True)
        except OSError:
            # Best-effort cleanup; log at call site if needed.
            pass
