from django.db import models
from django.core import validators
from django.core.files.storage import default_storage
from django.core.exceptions import ValidationError

from utils.db.validators import (
    PhoneNumberRegexValidator,
    FileExtensionValidator,
    validate_file_size,
    validate_mime_type,
    validate_file_content,
)

import json


class CustomFileField(models.FileField):
    """
    A custom file field that extends the default Django FileField with additional validation.
    """

    default_validators = [
        validate_file_size,
        validate_mime_type,
        validate_file_content,
        FileExtensionValidator(allowed_extensions=["jpg", "png", "pdf"]),
    ]

    def pre_save(self, model_instance, add):
        """
        Called before the model instance is saved.
        This method processes the file field before saving the instance.

        Parameters:
        - model_instance: The instance of the model being saved.
        - add: Boolean indicating if the instance is being added (True) or updated (False).

        Returns:
        - The file associated with the field.
        """
        file = super().pre_save(model_instance, add)
        # Additional logic if needed
        return file


class CustomImageField(models.ImageField):
    """
    A custom image field that extends the default Django ImageField.
    """

    default_validators = [
        validate_file_size,
        validate_mime_type,
        validate_file_content,
        FileExtensionValidator(allowed_extensions=["jpg", "png", "jpeg", "gif"]),
    ]

    def pre_save(self, model_instance, add):
        """
        Called before the model instance is saved.
        This method processes the image field before saving the instance.

        Parameters:
        - model_instance: The instance of the model being saved.
        - add: Boolean indicating if the instance is being added (True) or updated (False).

        Returns:
        - The image associated with the field.
        """
        file = super().pre_save(model_instance, add)
        # Add custom logic here if needed
        return file

    def delete(self, save=True):
        """
        Delete the image file from the storage.

        Args:
            save (bool): Whether to save the model instance after deleting the file.
        """
        if self and self.name and default_storage.exists(self.name):
            default_storage.delete(self.name)
        if save and self.instance:
            self.instance.save()


class PriceField(models.PositiveIntegerField):
    """
    A field for storing prices as positive integers.
    Default value is set to 0, and it is validated to ensure non-negative values.
    """

    def __init__(self, *args, **kwargs):
        kwargs["default"] = 0
        kwargs["validators"] = [validators.MinValueValidator(0)]
        super().__init__(*args, **kwargs)


class PercentField(models.FloatField):
    """
    A field for storing percentages as positive integers.
    Default value is set to 0, and it is validated to ensure values between 0 and 100.
    """

    def __init__(self, *args, **kwargs):
        kwargs["default"] = 0
        kwargs["validators"] = [
            validators.MinValueValidator(0),
            validators.MaxValueValidator(100),
        ]
        super().__init__(*args, **kwargs)


class ArrayField(models.TextField):
    """
    A custom ArrayField that stores a Python list in a TextField.
    It automatically serializes and deserializes the list to/from a JSON string.

    Attributes:
        base_type (type): The type of items allowed in the list (e.g., str, int).
        max_length (int): Optional maximum number of items in the list.
    """

    def __init__(self, *args, base_type=str, max_length=None, **kwargs):
        self.base_type = (
            base_type  # The type of items stored in the array (e.g., str, int)
        )
        self.max_length = max_length  # Max number of elements in the list
        super().__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection):
        """
        Convert the database string (JSON) back to a Python list when retrieving from the database.
        """
        if value is None:
            return []
        return json.loads(value)

    def to_python(self, value):
        """
        Convert value to Python (list) before saving or when accessed from a form.
        """
        if isinstance(value, list):
            return value  # It's already a list
        try:
            return json.loads(value)  # Try converting from JSON
        except (TypeError, ValueError):
            raise ValidationError(
                "Invalid input for ArrayField. Expecting a JSON string or list."
            )

    def get_prep_value(self, value):
        """
        Prepare the value for saving into the database (convert list to JSON string).
        """
        if value is None:
            return "[]"  # Default to empty list if None
        if not isinstance(value, list):
            raise ValidationError(f"Expected a list, got {type(value).__name__}.")
        return json.dumps(value)

    def validate(self, value, model_instance):
        """
        Validate that the value is a list of the correct type and within the allowed length.
        """
        if not isinstance(value, list):
            raise ValidationError(f"Expected a list, got {type(value).__name__}.")

        # Check length constraint
        if self.max_length and len(value) > self.max_length:
            raise ValidationError(
                f"List contains {len(value)} items, but the maximum is {self.max_length}."
            )

        # Check the type of each item in the list
        for item in value:
            if not isinstance(item, self.base_type):
                raise ValidationError(
                    f"All list items must be of type {self.base_type.__name__}, but got {type(item).__name__}."
                )

        super().validate(value, model_instance)

    def formfield(self, **kwargs):
        """
        Define the form field for the ArrayField (using a TextInput for now).
        """
        defaults = {"widget": models.TextField().formfield().widget}
        defaults.update(kwargs)
        return super().formfield(**defaults)


class PhoneField(models.CharField):
    """
    A field for storing phone numbers as character strings.
    It is validated against a regex pattern to ensure correct formatting.
    """

    def __init__(self, *args, **kwargs):
        kwargs["max_length"] = 11
        kwargs["validators"] = [PhoneNumberRegexValidator]
        super().__init__(*args, **kwargs)
