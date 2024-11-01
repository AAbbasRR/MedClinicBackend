from rest_framework import serializers

from utils.functions import get_client_ip
from utils.exceptions.rest import NotFoundObjectException


class CustomSerializer(serializers.Serializer):
    """
    A custom serializer base class that includes request and user handling,
    and provides access to client IP.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the serializer, setting up the request, user, and method context.
        """
        super().__init__(*args, **kwargs)
        self.request = self.context.get("request", None)
        if self.request:
            self.serializer_have_request_on_context(*args, **kwargs)
            self.user = self.request.user
            self.method = self.request.method
            self.serializer_after_access_to_method_and_user(*args, **kwargs)

    def serializer_have_request_on_context(self, *args, **kwargs):
        """
        Hook method to handle custom logic after request is set on context.
        Can be overridden in subclasses.
        """
        pass

    def serializer_after_access_to_method_and_user(self, *args, **kwargs):
        """
        Hook method to handle custom logic after access to user and method.
        Can be overridden in subclasses.
        """
        pass

    @property
    def client_ip(self):
        """
        Returns the client IP address from the request.

        Returns:
        -------
        str or None
            The client IP address, or None if request is not available.
        """
        return get_client_ip(self.request) if self.request else None


class CustomModelSerializer(serializers.ModelSerializer):
    """
    A custom model serializer base class with additional features for handling
    request context, user, and method, and for customizing field requirements.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the model serializer, setting up the request, user, and method context,
        and adjusting field requirements based on the request method.
        """
        super().__init__(*args, **kwargs)
        self.user = None
        self.request = self.context.get("request", None)
        if self.request:
            self.serializer_have_request_on_context(*args, **kwargs)
            self.user = self.request.user
            self.method = self.request.method
            self.serializer_after_access_to_method_and_user(*args, **kwargs)
            if self.method == "PATCH":
                self._update_field_requirements_for_patch()

    def serializer_have_request_on_context(self, *args, **kwargs):
        """
        Hook method to handle custom logic after request is set on context.
        Can be overridden in subclasses.
        """
        pass

    def serializer_after_access_to_method_and_user(self, *args, **kwargs):
        """
        Hook method to handle custom logic after access to user and method.
        Can be overridden in subclasses.
        """
        pass

    def _update_field_requirements_for_patch(self):
        """
        Updates the field requirements for PATCH requests based on the
        exclude_required_fields_for_update attribute.
        """
        exclude_required_fields_for_update = getattr(
            self.Meta, "exclude_required_fields_for_update", ()
        )
        for field_name, field in self.fields.items():
            if field_name not in exclude_required_fields_for_update:
                field.required = False
                field.allow_blank = True

    def get_find_object(self, model, pk, object_name=None, allow_null=False):
        """
        Retrieves an object from the database by primary key.

        Parameters:
        ----------
        model : Django model
            The model to query.
        pk : int or str
            The primary key of the object.
        object_name : str, optional
            The name of the object for exception messages.
        allow_null : bool, optional
            Whether to allow null values for the primary key.

        Returns:
        -------
        object
            The retrieved object.

        Raises:
        ------
        NotFoundObjectException
            If the object does not exist and allow_null is False.
        """
        if allow_null and pk is None:
            return None
        try:
            return model.objects.get(pk=pk)
        except model.DoesNotExist:
            raise NotFoundObjectException(
                object_name=object_name if object_name else model.__name__
            )

    @property
    def client_ip(self):
        """
        Returns the client IP address from the request.

        Returns:
        -------
        str or None
            The client IP address, or None if request is not available.
        """
        return get_client_ip(self.request) if self.request else None
