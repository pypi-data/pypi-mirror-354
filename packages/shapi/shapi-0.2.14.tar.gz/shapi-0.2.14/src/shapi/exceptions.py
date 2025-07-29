"""Custom exceptions for the shapi package."""


class shapiError(Exception):
    """Base exception for all shapi-related errors."""

    pass


class ConversionError(shapiError):
    """Raised when document conversion fails."""

    pass


class UnsupportedFormatError(shapiError):
    """Raised when an unsupported format is requested."""

    pass


class OCRProcessingError(shapiError):
    """Raised when OCR processing fails."""

    pass


class TemplateError(shapiError):
    """Raised when there's an error with document templates."""

    pass


class ValidationError(shapiError):
    """Raised when input validation fails."""

    pass
