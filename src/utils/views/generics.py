from django.shortcuts import get_object_or_404
from django.http import Http404

from rest_framework import generics, status, response

from utils.exceptions.rest import NotFoundObjectException, ParameterRequiredException


class BaseAPIView:
    """
    A base class to provide common functionality for custom API views.
    """

    lookup_fields = ["pk"]
    object_name = ""

    def get_filter(self):
        """
        Returns a filter dictionary based on request GET parameters.

        Returns:
        -------
        dict
            A dictionary with filter criteria.
        """
        filter = {}
        param_error = False
        for lookup_field in self.lookup_fields:
            param_value = self.request.GET.get(lookup_field)
            if param_value:
                filter[lookup_field] = param_value
                param_error = False
                break
            else:
                param_error = True
        if param_error:
            raise ParameterRequiredException(self.lookup_fields)
        return filter

    def get_object(self):
        """
        Retrieves the object based on filter criteria.

        Returns:
        -------
        object
            The object retrieved from the queryset.

        Raises:
        ------
        NotFoundObjectException
            If the object is not found in the queryset.
        """
        filter = self.get_filter()
        queryset = self.filter_queryset(self.get_queryset())
        try:
            return get_object_or_404(queryset, **filter)
        except Http404:
            raise NotFoundObjectException(object_name=self.object_name)


class CustomListAPIView(generics.ListAPIView):
    """
    Custom view for listing objects.
    """

    pass


class CustomListCreateAPIView(generics.ListCreateAPIView):
    """
    Custom view for listing and creating objects.
    """

    pass


class CustomCreateAPIView(generics.CreateAPIView):
    """
    Custom view for creating an object.
    """

    pass


class CustomRetrieveAPIView(BaseAPIView, generics.RetrieveAPIView):
    """
    Custom view for retrieving a single object.
    """

    pass


class CustomRetrieveUpdateAPIView(BaseAPIView, generics.RetrieveUpdateAPIView):
    """
    Custom view for retrieving and updating a single object.
    """

    http_method_names = ["get", "patch", "head", "options"]


class CustomRetrieveDestroyAPIView(BaseAPIView, generics.RetrieveDestroyAPIView):
    """
    Custom view for retrieving and deleting a single object.
    """

    pass


class CustomRetrieveUpdateDestroyAPIView(
    BaseAPIView, generics.RetrieveUpdateDestroyAPIView
):
    """
    Custom view for retrieving, updating, and deleting a single object.
    """

    http_method_names = ["get", "patch", "delete", "head", "options"]


class CustomUpdateAPIView(BaseAPIView, generics.UpdateAPIView):
    """
    Custom view for updating a single object.
    """

    pass


class CustomDestroyAPIView(BaseAPIView, generics.DestroyAPIView):
    """
    Custom view for deleting a single object.
    """

    def perform_destroy(self, instance):
        """
        Perform deletion and set the last modified user.

        Parameters:
        ----------
        instance : model instance
            The object to be deleted.
        """
        user = self.request.user
        if user.is_authenticated:
            instance.last_modified_by = user
        instance.delete()


class CustomUpdateDestroyAPIView(BaseAPIView, generics.RetrieveUpdateDestroyAPIView):
    """
    Custom view for updating and deleting a single object.
    """

    http_method_names = ["patch", "delete", "head", "options"]

    def perform_destroy(self, instance):
        """
        Perform deletion and set the last modified user.

        Parameters:
        ----------
        instance : model instance
            The object to be deleted.
        """
        user = self.request.user
        if user.is_authenticated:
            instance.last_modified_by = user
        instance.delete()


class CustomGenericAPIView(generics.GenericAPIView):
    """
    Base class for custom generic views.
    """

    pass


class CustomGenericPostAPIView(CustomGenericAPIView):
    """
    Custom view for handling POST requests.
    """

    def post(self, request, *args, **kwargs):
        """
        Handle POST request to create or process data.

        Parameters:
        ----------
        request : Request
            The HTTP request object.

        Returns:
        -------
        Response
            The response with the serialized data.
        """
        ser = self.get_serializer(data=self.request.data)
        if ser.is_valid(raise_exception=True):
            return response.Response(ser.validated_data, status=status.HTTP_200_OK)


class CustomGenericGetAPIView(CustomGenericAPIView):
    """
    Custom view for handling GET requests.
    """

    serializable_object = None

    def get_serializable_object(self):
        """
        Retrieve the object to be serialized.

        Returns:
        -------
        object
            The object to be serialized.
        """
        return self.serializable_object

    def get(self, *args, **kwargs):
        """
        Handle GET request to retrieve data.

        Parameters:
        ----------
        request : Request
            The HTTP request object.

        Returns:
        -------
        Response
            The response with the serialized data.
        """
        ser = self.get_serializer(self.get_serializable_object())
        return response.Response(ser.data)
