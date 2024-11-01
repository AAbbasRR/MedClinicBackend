from rest_framework.versioning import URLPathVersioning


class BaseVersioning(URLPathVersioning):
    """
    Custom versioning class that extends `URLPathVersioning` to manage API versions
    via URL path.

    Attributes:
    ----------
    default_version : str
        The default version to use if no version is provided in the request.
    allowed_versions : list
        A list of allowed API versions.
    """

    default_version = "v1"
    allowed_versions = ["v1"]

    def get_version(self, request):
        """
        Retrieve the API version from the URL path.

        Parameters:
        ----------
        request : Request
            The HTTP request object.

        Returns:
        -------
        str
            The version of the API as specified in the URL path.
        """
        version = super().get_version(request)
        if version not in self.allowed_versions:
            raise ValueError(
                f"Version '{version}' is not allowed. Allowed versions are: {self.allowed_versions}"
            )
        return version
