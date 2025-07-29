import os

from flexrag.utils import configure

from .document_parser_base import DOCUMENTPARSERS, Document, DocumentParserBase


@configure
class DoclingConfig:
    do_ocr: bool = False
    do_table_structure: bool = True
    generate_page_images: bool = False
    generate_picture_images: bool = False


@DOCUMENTPARSERS("docling", config_class=DoclingConfig)
class DoclingParser(DocumentParserBase):
    def __init__(self, config: DoclingConfig):
        try:
            from docling.datamodel.base_models import InputFormat
            from docling.datamodel.pipeline_options import PdfPipelineOptions
            from docling.document_converter import DocumentConverter, PdfFormatOption
        except ImportError:
            raise ImportError(
                "Docling is not installed. Please install it via `pip install docling`."
            )

        pdf_pipeline_options = PdfPipelineOptions(
            do_ocr=config.do_ocr,
            do_table_structure=config.do_table_structure,
            generate_page_images=config.generate_page_images,
            generate_picture_images=config.generate_picture_images,
        )
        self.doc_converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pdf_pipeline_options)
            }
        )
        return

    def parse(self, input_file_path: str) -> Document:
        assert os.path.exists(input_file_path)
        document_ = self.doc_converter.convert(input_file_path).document
        document = Document(
            source_file_path=input_file_path,
            text=document_.export_to_markdown(),
            title=document_.name,
        )
        if document.pagaes.image is not None:
            document.screenshots = [p.image.pil_image for p in document_.pages]
        if document.pictures.image is not None:
            document.images = [p.image.pil_image for p in document_.pictures]
        return document
