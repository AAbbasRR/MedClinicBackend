from rest_framework.validators import UniqueValidator as DjangoUniqueValidator
from django.core.validators import (
    RegexValidator,
    ValidationError,
    FileExtensionValidator,
)

from utils.base_errors import BaseErrors

from mimetypes import guess_type

# Regex pattern for validating phone numbers
PhoneRegex = r"^(0?9[0-9]{9})$"
# Regex pattern for validating emails
EmailRegex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

# Validator for phone numbers based on the defined regex
PhoneNumberRegexValidator = RegexValidator(
    PhoneRegex, message=BaseErrors.invalid_mobile_number_format
)

# Validator for emails based on the defined regex
EmailRegexValidator = RegexValidator(EmailRegex, BaseErrors.invalid_email_format)


class UniqueValidator(DjangoUniqueValidator):
    message = BaseErrors.unique_field


def validate_file_size(file):
    """Check that the file size is not too large."""
    max_size_kb = 5120  # 5 MB
    if file.size > max_size_kb * 1024:
        raise ValidationError(f"File size cannot exceed {max_size_kb} KB.")


def validate_mime_type(file):
    """Check that the file has a valid MIME type."""
    allowed_mime_types = ["image/jpeg", "image/png", "application/pdf"]
    mime_type, _ = guess_type(file.name)
    if mime_type not in allowed_mime_types:
        raise ValidationError(
            f"Invalid file type: {mime_type}. Allowed types are: {', '.join(allowed_mime_types)}."
        )


def validate_file_content(file):
    """Check that the file content is not corrupt."""
    try:
        # Try to read the file's content to ensure it's not corrupted
        file.open("rb")  # Open the file in binary mode
        file.read()
        file.seek(0)  # Reset the file pointer to the beginning of the file
    except Exception as e:
        raise ValidationError(f"Could not read the file content: {e}")
