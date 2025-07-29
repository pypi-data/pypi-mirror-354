"""

        ComPDFKit Conversion python3 SDK
    
"""
from __future__ import annotations
import typing
__all__ = ['AUTO', 'BINARY', 'BMP', 'BOX', 'CANCEL', 'CHINESE', 'CHINESE_TRA', 'COLOR', 'COMPRESS_ERROR', 'CONVERTING_ERROR', 'CPDFConversion', 'ConvertOptions', 'DEVANAGARI', 'ENGLISH', 'ErrorCode', 'ExcelWorksheetOption', 'FILE_ERROR', 'FLOW', 'FOR_DOCUMENT', 'FOR_PAGE', 'FOR_TABLE', 'GRAY', 'HtmlOption', 'IO_ERROR', 'ImageColorMode', 'ImageType', 'JAPANESE', 'JPEG', 'JPG', 'KOREAN', 'LATIN', 'LICENSE_EXPIRE', 'LICENSE_FILE_READ_FAILED', 'LICENSE_ILLEGAL_ACCESS', 'LICENSE_INVALID', 'LICENSE_OCR_PERMISSION_DENY', 'LICENSE_PERMISSION_DENY', 'LICENSE_UNINITIALIZED', 'LICENSE_UNSUPPORTED_DEVICE', 'LICENSE_UNSUPPORTED_ID', 'LICENSE_UNSUPPORTED_PLATFORM', 'LibraryManager', 'MULTIPLE_PAGE', 'MULTIPLE_PAGE_WITH_BOOKMARK', 'NO_TABLE_ERROR', 'OCRLanguage', 'OCR_FAILURE', 'OUT_OF_MEMORY', 'PDF_FORMAT_ERROR', 'PDF_PAGE_ERROR', 'PDF_PASSWORD_ERROR', 'PDF_SECURITY_ERROR', 'PNG', 'PageLayoutMode', 'SINGLE_PAGE', 'SINGLE_PAGE_WITH_BOOKMARK', 'SUCCESS', 'TIFF', 'UNKNOWN', 'UNKNOWN_ERROR']
class CPDFConversion:
    """
    
        CPDFConversion class provides functionalities to convert PDF files into various formats such as Word, Excel, PPT, HTML, etc.
    """
    @staticmethod
    def cancel() -> None:
        """
        Cancels any ongoing PDF conversion process.
        """
    @staticmethod
    def start_pdf_to_excel(file_path: str, password: str, output_path: str, options: ConvertOptions) -> ErrorCode:
        """
        Starts the conversion of a PDF file to an Excel document.
        """
    @staticmethod
    def start_pdf_to_html(file_path: str, password: str, output_path: str, options: ConvertOptions) -> ErrorCode:
        """
        Starts the conversion of a PDF file to an HTML document.
        """
    @staticmethod
    def start_pdf_to_image(file_path: str, password: str, output_path: str, options: ConvertOptions) -> ErrorCode:
        """
        Starts the conversion of a PDF file to an image format.
        """
    @staticmethod
    def start_pdf_to_json(file_path: str, password: str, output_path: str, options: ConvertOptions) -> ErrorCode:
        """
        Starts the conversion of a PDF file to a JSON document.
        """
    @staticmethod
    def start_pdf_to_markdown(file_path: str, password: str, output_path: str, options: ConvertOptions) -> ErrorCode:
        """
        Starts the conversion of a PDF file to a Markdown document.
        """
    @staticmethod
    def start_pdf_to_ppt(file_path: str, password: str, output_path: str, options: ConvertOptions) -> ErrorCode:
        """
        Starts the conversion of a PDF file to a PowerPoint presentation.
        """
    @staticmethod
    def start_pdf_to_rtf(file_path: str, password: str, output_path: str, options: ConvertOptions) -> ErrorCode:
        """
        Starts the conversion of a PDF file to an RTF document.
        """
    @staticmethod
    def start_pdf_to_searchable_pdf(file_path: str, password: str, output_path: str, options: ConvertOptions) -> ErrorCode:
        """
        Starts the conversion of a PDF file to a searchable PDF document.
        """
    @staticmethod
    def start_pdf_to_txt(file_path: str, password: str, output_path: str, options: ConvertOptions) -> ErrorCode:
        """
        Starts the conversion of a PDF file to a plain text file.
        """
    @staticmethod
    def start_pdf_to_word(file_path: str, password: str, output_path: str, options: ConvertOptions) -> ErrorCode:
        """
        Starts the conversion of a PDF file to a Word document.
        """
class ConvertOptions:
    def __init__(self) -> None:
        """
        Default constructor
        """
    def __repr__(self) -> str:
        """
        String representation of ConvertOptions object
        """
    def __str__(self) -> str:
        """
        String representation of ConvertOptions object
        """
    @property
    def contain_annotation(self) -> bool:
        """
        Whether to contain annotations when converting
        """
    @contain_annotation.setter
    def contain_annotation(self, arg0: bool) -> None:
        ...
    @property
    def contain_image(self) -> bool:
        """
        Whether to contain images when converting, which takes effect only when IsAllowOCR is false
        """
    @contain_image.setter
    def contain_image(self, arg0: bool) -> None:
        ...
    @property
    def enable_ai_layout(self) -> bool:
        """
        Whether to enable AI layout analysis during conversion
        """
    @enable_ai_layout.setter
    def enable_ai_layout(self, arg0: bool) -> None:
        ...
    @property
    def enable_ocr(self) -> bool:
        """
        Whether to use OCR
        """
    @enable_ocr.setter
    def enable_ocr(self, arg0: bool) -> None:
        ...
    @property
    def excel_all_content(self) -> bool:
        """
        Whether to set contain all pdf content to the xlsx file
        """
    @excel_all_content.setter
    def excel_all_content(self, arg0: bool) -> None:
        ...
    @property
    def excel_csv_format(self) -> bool:
        """
        Whether to set to save the table in csv format
        """
    @excel_csv_format.setter
    def excel_csv_format(self, arg0: bool) -> None:
        ...
    @property
    def excel_worksheet_option(self) -> ExcelWorksheetOption:
        """
        Specify the Excel worksheet option for conversion
        """
    @excel_worksheet_option.setter
    def excel_worksheet_option(self, arg0: ExcelWorksheetOption) -> None:
        ...
    @property
    def formula_to_image(self) -> bool:
        """
        Whether to convert formula to image
        """
    @formula_to_image.setter
    def formula_to_image(self, arg0: bool) -> None:
        ...
    @property
    def html_option(self) -> HtmlOption:
        """
        Specify the HTML option for conversion
        """
    @html_option.setter
    def html_option(self, arg0: HtmlOption) -> None:
        ...
    @property
    def image_color_mode(self) -> ImageColorMode:
        """
        Specify the image color mode of the image file
        """
    @image_color_mode.setter
    def image_color_mode(self, arg0: ImageColorMode) -> None:
        ...
    @property
    def image_path_enhance(self) -> bool:
        """
        Whether to enhance the image path
        """
    @image_path_enhance.setter
    def image_path_enhance(self, arg0: bool) -> None:
        ...
    @property
    def image_scaling(self) -> float:
        """
        Specify the image scaling of the image file
        """
    @image_scaling.setter
    def image_scaling(self, arg0: float) -> None:
        ...
    @property
    def image_type(self) -> ImageType:
        """
        Specify the image type of the image file
        """
    @image_type.setter
    def image_type(self, arg0: ImageType) -> None:
        ...
    @property
    def json_contain_table(self) -> bool:
        """
        Whether to contain table when convert pdf to json
        """
    @json_contain_table.setter
    def json_contain_table(self, arg0: bool) -> None:
        ...
    @property
    def page_layout_mode(self) -> PageLayoutMode:
        """
        Specify the layout mode
        """
    @page_layout_mode.setter
    def page_layout_mode(self, arg0: PageLayoutMode) -> None:
        ...
    @property
    def page_ranges(self) -> str:
        """
        Specify the pages to convert, e.g. "1-3,5,7-9"
        """
    @page_ranges.setter
    def page_ranges(self, arg0: str) -> None:
        ...
    @property
    def txt_table_format(self) -> bool:
        """
        Whether format table when convert pdf to txt
        """
    @txt_table_format.setter
    def txt_table_format(self, arg0: bool) -> None:
        ...
class ErrorCode:
    """
    Members:
    
      SUCCESS : Success, and no error occurs
    
      CANCEL : Conversion process was canceled
    
      FILE_ERROR : File cannot be found or could not be opened
    
      PDF_PASSWORD_ERROR : Invalid password. Usually, this error may occur when loading a PDF document with password. When meet this, user should load document again with correct password
    
      PDF_PAGE_ERROR : PDF page failed to load
    
      PDF_FORMAT_ERROR : Format is invalid. For files, this may also mean that file is corrupted
    
      PDF_SECURITY_ERROR : PDF document is encrypted by some unsupported security handler
    
      OUT_OF_MEMORY : Out-of-memory error occurs
    
      IO_ERROR : System I/O error
    
      COMPRESS_ERROR : Folder compression failed
    
      LICENSE_INVALID : The license is invalid
    
      LICENSE_EXPIRE : The license has expired
    
      LICENSE_UNSUPPORTED_PLATFORM : The license does not support the current platform
    
      LICENSE_UNSUPPORTED_ID : The license does not support the application id
    
      LICENSE_UNSUPPORTED_DEVICE : The license does not support the device id
    
      LICENSE_PERMISSION_DENY : The license does not have the function permission
    
      LICENSE_UNINITIALIZED : The license has not been initialized
    
      LICENSE_ILLEGAL_ACCESS : Illegal access to the API interface
    
      LICENSE_FILE_READ_FAILED : Failed to read license file
    
      LICENSE_OCR_PERMISSION_DENY : The license does not have OCR permissions
    
      NO_TABLE_ERROR : No tables found in the source file
    
      OCR_FAILURE : Failed to call OCR recognition
    
      CONVERTING_ERROR : Currently executing conversion task
    
      UNKNOWN_ERROR : Unknown error
    """
    CANCEL: typing.ClassVar[ErrorCode]  # value = <ErrorCode.CANCEL: 1>
    COMPRESS_ERROR: typing.ClassVar[ErrorCode]  # value = <ErrorCode.COMPRESS_ERROR: 9>
    CONVERTING_ERROR: typing.ClassVar[ErrorCode]  # value = <ErrorCode.CONVERTING_ERROR: 60>
    FILE_ERROR: typing.ClassVar[ErrorCode]  # value = <ErrorCode.FILE_ERROR: 2>
    IO_ERROR: typing.ClassVar[ErrorCode]  # value = <ErrorCode.IO_ERROR: 8>
    LICENSE_EXPIRE: typing.ClassVar[ErrorCode]  # value = <ErrorCode.LICENSE_EXPIRE: 21>
    LICENSE_FILE_READ_FAILED: typing.ClassVar[ErrorCode]  # value = <ErrorCode.LICENSE_FILE_READ_FAILED: 28>
    LICENSE_ILLEGAL_ACCESS: typing.ClassVar[ErrorCode]  # value = <ErrorCode.LICENSE_ILLEGAL_ACCESS: 27>
    LICENSE_INVALID: typing.ClassVar[ErrorCode]  # value = <ErrorCode.LICENSE_INVALID: 20>
    LICENSE_OCR_PERMISSION_DENY: typing.ClassVar[ErrorCode]  # value = <ErrorCode.LICENSE_OCR_PERMISSION_DENY: 29>
    LICENSE_PERMISSION_DENY: typing.ClassVar[ErrorCode]  # value = <ErrorCode.LICENSE_PERMISSION_DENY: 25>
    LICENSE_UNINITIALIZED: typing.ClassVar[ErrorCode]  # value = <ErrorCode.LICENSE_UNINITIALIZED: 26>
    LICENSE_UNSUPPORTED_DEVICE: typing.ClassVar[ErrorCode]  # value = <ErrorCode.LICENSE_UNSUPPORTED_DEVICE: 24>
    LICENSE_UNSUPPORTED_ID: typing.ClassVar[ErrorCode]  # value = <ErrorCode.LICENSE_UNSUPPORTED_ID: 23>
    LICENSE_UNSUPPORTED_PLATFORM: typing.ClassVar[ErrorCode]  # value = <ErrorCode.LICENSE_UNSUPPORTED_PLATFORM: 22>
    NO_TABLE_ERROR: typing.ClassVar[ErrorCode]  # value = <ErrorCode.NO_TABLE_ERROR: 40>
    OCR_FAILURE: typing.ClassVar[ErrorCode]  # value = <ErrorCode.OCR_FAILURE: 41>
    OUT_OF_MEMORY: typing.ClassVar[ErrorCode]  # value = <ErrorCode.OUT_OF_MEMORY: 7>
    PDF_FORMAT_ERROR: typing.ClassVar[ErrorCode]  # value = <ErrorCode.PDF_FORMAT_ERROR: 5>
    PDF_PAGE_ERROR: typing.ClassVar[ErrorCode]  # value = <ErrorCode.PDF_PAGE_ERROR: 4>
    PDF_PASSWORD_ERROR: typing.ClassVar[ErrorCode]  # value = <ErrorCode.PDF_PASSWORD_ERROR: 3>
    PDF_SECURITY_ERROR: typing.ClassVar[ErrorCode]  # value = <ErrorCode.PDF_SECURITY_ERROR: 6>
    SUCCESS: typing.ClassVar[ErrorCode]  # value = <ErrorCode.SUCCESS: 0>
    UNKNOWN_ERROR: typing.ClassVar[ErrorCode]  # value = <ErrorCode.UNKNOWN_ERROR: 100>
    __members__: typing.ClassVar[dict[str, ErrorCode]]  # value = {'SUCCESS': <ErrorCode.SUCCESS: 0>, 'CANCEL': <ErrorCode.CANCEL: 1>, 'FILE_ERROR': <ErrorCode.FILE_ERROR: 2>, 'PDF_PASSWORD_ERROR': <ErrorCode.PDF_PASSWORD_ERROR: 3>, 'PDF_PAGE_ERROR': <ErrorCode.PDF_PAGE_ERROR: 4>, 'PDF_FORMAT_ERROR': <ErrorCode.PDF_FORMAT_ERROR: 5>, 'PDF_SECURITY_ERROR': <ErrorCode.PDF_SECURITY_ERROR: 6>, 'OUT_OF_MEMORY': <ErrorCode.OUT_OF_MEMORY: 7>, 'IO_ERROR': <ErrorCode.IO_ERROR: 8>, 'COMPRESS_ERROR': <ErrorCode.COMPRESS_ERROR: 9>, 'LICENSE_INVALID': <ErrorCode.LICENSE_INVALID: 20>, 'LICENSE_EXPIRE': <ErrorCode.LICENSE_EXPIRE: 21>, 'LICENSE_UNSUPPORTED_PLATFORM': <ErrorCode.LICENSE_UNSUPPORTED_PLATFORM: 22>, 'LICENSE_UNSUPPORTED_ID': <ErrorCode.LICENSE_UNSUPPORTED_ID: 23>, 'LICENSE_UNSUPPORTED_DEVICE': <ErrorCode.LICENSE_UNSUPPORTED_DEVICE: 24>, 'LICENSE_PERMISSION_DENY': <ErrorCode.LICENSE_PERMISSION_DENY: 25>, 'LICENSE_UNINITIALIZED': <ErrorCode.LICENSE_UNINITIALIZED: 26>, 'LICENSE_ILLEGAL_ACCESS': <ErrorCode.LICENSE_ILLEGAL_ACCESS: 27>, 'LICENSE_FILE_READ_FAILED': <ErrorCode.LICENSE_FILE_READ_FAILED: 28>, 'LICENSE_OCR_PERMISSION_DENY': <ErrorCode.LICENSE_OCR_PERMISSION_DENY: 29>, 'NO_TABLE_ERROR': <ErrorCode.NO_TABLE_ERROR: 40>, 'OCR_FAILURE': <ErrorCode.OCR_FAILURE: 41>, 'CONVERTING_ERROR': <ErrorCode.CONVERTING_ERROR: 60>, 'UNKNOWN_ERROR': <ErrorCode.UNKNOWN_ERROR: 100>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class ExcelWorksheetOption:
    """
    Members:
    
      FOR_TABLE : A worksheet to contain only one table
    
      FOR_PAGE : A worksheet to contain table for PDF Page
    
      FOR_DOCUMENT : A worksheet to contain table for PDF Document
    """
    FOR_DOCUMENT: typing.ClassVar[ExcelWorksheetOption]  # value = <ExcelWorksheetOption.FOR_DOCUMENT: 2>
    FOR_PAGE: typing.ClassVar[ExcelWorksheetOption]  # value = <ExcelWorksheetOption.FOR_PAGE: 1>
    FOR_TABLE: typing.ClassVar[ExcelWorksheetOption]  # value = <ExcelWorksheetOption.FOR_TABLE: 0>
    __members__: typing.ClassVar[dict[str, ExcelWorksheetOption]]  # value = {'FOR_TABLE': <ExcelWorksheetOption.FOR_TABLE: 0>, 'FOR_PAGE': <ExcelWorksheetOption.FOR_PAGE: 1>, 'FOR_DOCUMENT': <ExcelWorksheetOption.FOR_DOCUMENT: 2>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class HtmlOption:
    """
    Members:
    
      SINGLE_PAGE : Convert the entire PDF file into a single HTML file
    
      SINGLE_PAGE_WITH_BOOKMARK : Convert the PDF file into a single HTML file with an outline for navigation at the beginning of the HTML page
    
      MULTIPLE_PAGE : Convert the PDF file into multiple HTML files
    
      MULTIPLE_PAGE_WITH_BOOKMARK : Convert the PDF file into multiple HTML files. Each HTML file corresponds to a PDF page, and users can navigate to the next HTML file via a link at the bottom of the HTML page
    """
    MULTIPLE_PAGE: typing.ClassVar[HtmlOption]  # value = <HtmlOption.MULTIPLE_PAGE: 2>
    MULTIPLE_PAGE_WITH_BOOKMARK: typing.ClassVar[HtmlOption]  # value = <HtmlOption.MULTIPLE_PAGE_WITH_BOOKMARK: 3>
    SINGLE_PAGE: typing.ClassVar[HtmlOption]  # value = <HtmlOption.SINGLE_PAGE: 0>
    SINGLE_PAGE_WITH_BOOKMARK: typing.ClassVar[HtmlOption]  # value = <HtmlOption.SINGLE_PAGE_WITH_BOOKMARK: 1>
    __members__: typing.ClassVar[dict[str, HtmlOption]]  # value = {'SINGLE_PAGE': <HtmlOption.SINGLE_PAGE: 0>, 'SINGLE_PAGE_WITH_BOOKMARK': <HtmlOption.SINGLE_PAGE_WITH_BOOKMARK: 1>, 'MULTIPLE_PAGE': <HtmlOption.MULTIPLE_PAGE: 2>, 'MULTIPLE_PAGE_WITH_BOOKMARK': <HtmlOption.MULTIPLE_PAGE_WITH_BOOKMARK: 3>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class ImageColorMode:
    """
    Members:
    
      COLOR : Color mode
    
      GRAY : Gray mode
    
      BINARY : Binary mode
    """
    BINARY: typing.ClassVar[ImageColorMode]  # value = <ImageColorMode.BINARY: 2>
    COLOR: typing.ClassVar[ImageColorMode]  # value = <ImageColorMode.COLOR: 0>
    GRAY: typing.ClassVar[ImageColorMode]  # value = <ImageColorMode.GRAY: 1>
    __members__: typing.ClassVar[dict[str, ImageColorMode]]  # value = {'COLOR': <ImageColorMode.COLOR: 0>, 'GRAY': <ImageColorMode.GRAY: 1>, 'BINARY': <ImageColorMode.BINARY: 2>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class ImageType:
    """
    Members:
    
      JPG : .jpg
    
      JPEG : .jpeg
    
      PNG : .png
    
      BMP : .bmp
    
      TIFF : .tiff
    """
    BMP: typing.ClassVar[ImageType]  # value = <ImageType.BMP: 3>
    JPEG: typing.ClassVar[ImageType]  # value = <ImageType.JPEG: 1>
    JPG: typing.ClassVar[ImageType]  # value = <ImageType.JPG: 0>
    PNG: typing.ClassVar[ImageType]  # value = <ImageType.PNG: 2>
    TIFF: typing.ClassVar[ImageType]  # value = <ImageType.TIFF: 4>
    __members__: typing.ClassVar[dict[str, ImageType]]  # value = {'JPG': <ImageType.JPG: 0>, 'JPEG': <ImageType.JPEG: 1>, 'PNG': <ImageType.PNG: 2>, 'BMP': <ImageType.BMP: 3>, 'TIFF': <ImageType.TIFF: 4>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class LibraryManager:
    """
    The `LibraryManager` class serves as a central hub for managing the lifecycle of an SDK library. It provides functionalities such as initializing the library with specified resources, verifying licenses, installing fonts, setting up logging and progress callbacks, retrieving version information, and counting pages in documents.
    """
    @staticmethod
    def get_page_count(file_path: str, password: str) -> int:
        """
        Returns the number of pages in a document.
        """
    @staticmethod
    def get_version(version: str) -> None:
        """
        Gets the version of the SDK library.
        """
    @staticmethod
    def initialize(resource_path: str) -> None:
        """
        Initializes the SDK library with the given resource path
        """
    @staticmethod
    def license_verify(license: str, device_id: str, app_id: str) -> ErrorCode:
        """
        Verifies the provided license key along with device ID and application ID.
        """
    @staticmethod
    def release() -> None:
        """
        Releases all resources used by the library. Should be called when the SDK is no longer needed.
        """
    @staticmethod
    def set_document_ai_model(file_path: str, language: OCRLanguage) -> ErrorCode:
        """
        Sets the Document AI model for OCR based on the provided file path and language.
        """
    @staticmethod
    def set_logger(enable_info: bool, enable_warning: bool) -> None:
        """
        Enables or disables logging for info and warning messages.
        """
    @staticmethod
    def set_ocr_language(language: OCRLanguage) -> None:
        """
        Sets the OCR language for document processing.
        """
    @staticmethod
    def set_progress(progress: typing.Callable) -> None:
        """
        Sets a callback function to track the progress of SDK operations.
        """
class OCRLanguage:
    """
    Members:
    
      UNKNOWN : Unknown language
    
      CHINESE : Chinese (Simplified)
    
      CHINESE_TRA : Chinese (Traditional)
    
      ENGLISH : English
    
      KOREAN : Korean
    
      JAPANESE : Japanese
    
      LATIN : Latin
    
      DEVANAGARI : Devanagari
    
      AUTO : Automatically select language
    """
    AUTO: typing.ClassVar[OCRLanguage]  # value = <OCRLanguage.AUTO: 8>
    CHINESE: typing.ClassVar[OCRLanguage]  # value = <OCRLanguage.CHINESE: 1>
    CHINESE_TRA: typing.ClassVar[OCRLanguage]  # value = <OCRLanguage.CHINESE_TRA: 2>
    DEVANAGARI: typing.ClassVar[OCRLanguage]  # value = <OCRLanguage.DEVANAGARI: 7>
    ENGLISH: typing.ClassVar[OCRLanguage]  # value = <OCRLanguage.ENGLISH: 3>
    JAPANESE: typing.ClassVar[OCRLanguage]  # value = <OCRLanguage.JAPANESE: 5>
    KOREAN: typing.ClassVar[OCRLanguage]  # value = <OCRLanguage.KOREAN: 4>
    LATIN: typing.ClassVar[OCRLanguage]  # value = <OCRLanguage.LATIN: 6>
    UNKNOWN: typing.ClassVar[OCRLanguage]  # value = <OCRLanguage.UNKNOWN: 0>
    __members__: typing.ClassVar[dict[str, OCRLanguage]]  # value = {'UNKNOWN': <OCRLanguage.UNKNOWN: 0>, 'CHINESE': <OCRLanguage.CHINESE: 1>, 'CHINESE_TRA': <OCRLanguage.CHINESE_TRA: 2>, 'ENGLISH': <OCRLanguage.ENGLISH: 3>, 'KOREAN': <OCRLanguage.KOREAN: 4>, 'JAPANESE': <OCRLanguage.JAPANESE: 5>, 'LATIN': <OCRLanguage.LATIN: 6>, 'DEVANAGARI': <OCRLanguage.DEVANAGARI: 7>, 'AUTO': <OCRLanguage.AUTO: 8>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
class PageLayoutMode:
    """
    Members:
    
      BOX : Box mode
    
      FLOW : Flowing mode
    """
    BOX: typing.ClassVar[PageLayoutMode]  # value = <PageLayoutMode.BOX: 0>
    FLOW: typing.ClassVar[PageLayoutMode]  # value = <PageLayoutMode.FLOW: 1>
    __members__: typing.ClassVar[dict[str, PageLayoutMode]]  # value = {'BOX': <PageLayoutMode.BOX: 0>, 'FLOW': <PageLayoutMode.FLOW: 1>}
    def __eq__(self, other: typing.Any) -> bool:
        ...
    def __getstate__(self) -> int:
        ...
    def __hash__(self) -> int:
        ...
    def __index__(self) -> int:
        ...
    def __init__(self, value: int) -> None:
        ...
    def __int__(self) -> int:
        ...
    def __ne__(self, other: typing.Any) -> bool:
        ...
    def __repr__(self) -> str:
        ...
    def __setstate__(self, state: int) -> None:
        ...
    def __str__(self) -> str:
        ...
    @property
    def name(self) -> str:
        ...
    @property
    def value(self) -> int:
        ...
AUTO: OCRLanguage  # value = <OCRLanguage.AUTO: 8>
BINARY: ImageColorMode  # value = <ImageColorMode.BINARY: 2>
BMP: ImageType  # value = <ImageType.BMP: 3>
BOX: PageLayoutMode  # value = <PageLayoutMode.BOX: 0>
CANCEL: ErrorCode  # value = <ErrorCode.CANCEL: 1>
CHINESE: OCRLanguage  # value = <OCRLanguage.CHINESE: 1>
CHINESE_TRA: OCRLanguage  # value = <OCRLanguage.CHINESE_TRA: 2>
COLOR: ImageColorMode  # value = <ImageColorMode.COLOR: 0>
COMPRESS_ERROR: ErrorCode  # value = <ErrorCode.COMPRESS_ERROR: 9>
CONVERTING_ERROR: ErrorCode  # value = <ErrorCode.CONVERTING_ERROR: 60>
DEVANAGARI: OCRLanguage  # value = <OCRLanguage.DEVANAGARI: 7>
ENGLISH: OCRLanguage  # value = <OCRLanguage.ENGLISH: 3>
FILE_ERROR: ErrorCode  # value = <ErrorCode.FILE_ERROR: 2>
FLOW: PageLayoutMode  # value = <PageLayoutMode.FLOW: 1>
FOR_DOCUMENT: ExcelWorksheetOption  # value = <ExcelWorksheetOption.FOR_DOCUMENT: 2>
FOR_PAGE: ExcelWorksheetOption  # value = <ExcelWorksheetOption.FOR_PAGE: 1>
FOR_TABLE: ExcelWorksheetOption  # value = <ExcelWorksheetOption.FOR_TABLE: 0>
GRAY: ImageColorMode  # value = <ImageColorMode.GRAY: 1>
IO_ERROR: ErrorCode  # value = <ErrorCode.IO_ERROR: 8>
JAPANESE: OCRLanguage  # value = <OCRLanguage.JAPANESE: 5>
JPEG: ImageType  # value = <ImageType.JPEG: 1>
JPG: ImageType  # value = <ImageType.JPG: 0>
KOREAN: OCRLanguage  # value = <OCRLanguage.KOREAN: 4>
LATIN: OCRLanguage  # value = <OCRLanguage.LATIN: 6>
LICENSE_EXPIRE: ErrorCode  # value = <ErrorCode.LICENSE_EXPIRE: 21>
LICENSE_FILE_READ_FAILED: ErrorCode  # value = <ErrorCode.LICENSE_FILE_READ_FAILED: 28>
LICENSE_ILLEGAL_ACCESS: ErrorCode  # value = <ErrorCode.LICENSE_ILLEGAL_ACCESS: 27>
LICENSE_INVALID: ErrorCode  # value = <ErrorCode.LICENSE_INVALID: 20>
LICENSE_OCR_PERMISSION_DENY: ErrorCode  # value = <ErrorCode.LICENSE_OCR_PERMISSION_DENY: 29>
LICENSE_PERMISSION_DENY: ErrorCode  # value = <ErrorCode.LICENSE_PERMISSION_DENY: 25>
LICENSE_UNINITIALIZED: ErrorCode  # value = <ErrorCode.LICENSE_UNINITIALIZED: 26>
LICENSE_UNSUPPORTED_DEVICE: ErrorCode  # value = <ErrorCode.LICENSE_UNSUPPORTED_DEVICE: 24>
LICENSE_UNSUPPORTED_ID: ErrorCode  # value = <ErrorCode.LICENSE_UNSUPPORTED_ID: 23>
LICENSE_UNSUPPORTED_PLATFORM: ErrorCode  # value = <ErrorCode.LICENSE_UNSUPPORTED_PLATFORM: 22>
MULTIPLE_PAGE: HtmlOption  # value = <HtmlOption.MULTIPLE_PAGE: 2>
MULTIPLE_PAGE_WITH_BOOKMARK: HtmlOption  # value = <HtmlOption.MULTIPLE_PAGE_WITH_BOOKMARK: 3>
NO_TABLE_ERROR: ErrorCode  # value = <ErrorCode.NO_TABLE_ERROR: 40>
OCR_FAILURE: ErrorCode  # value = <ErrorCode.OCR_FAILURE: 41>
OUT_OF_MEMORY: ErrorCode  # value = <ErrorCode.OUT_OF_MEMORY: 7>
PDF_FORMAT_ERROR: ErrorCode  # value = <ErrorCode.PDF_FORMAT_ERROR: 5>
PDF_PAGE_ERROR: ErrorCode  # value = <ErrorCode.PDF_PAGE_ERROR: 4>
PDF_PASSWORD_ERROR: ErrorCode  # value = <ErrorCode.PDF_PASSWORD_ERROR: 3>
PDF_SECURITY_ERROR: ErrorCode  # value = <ErrorCode.PDF_SECURITY_ERROR: 6>
PNG: ImageType  # value = <ImageType.PNG: 2>
SINGLE_PAGE: HtmlOption  # value = <HtmlOption.SINGLE_PAGE: 0>
SINGLE_PAGE_WITH_BOOKMARK: HtmlOption  # value = <HtmlOption.SINGLE_PAGE_WITH_BOOKMARK: 1>
SUCCESS: ErrorCode  # value = <ErrorCode.SUCCESS: 0>
TIFF: ImageType  # value = <ImageType.TIFF: 4>
UNKNOWN: OCRLanguage  # value = <OCRLanguage.UNKNOWN: 0>
UNKNOWN_ERROR: ErrorCode  # value = <ErrorCode.UNKNOWN_ERROR: 100>
