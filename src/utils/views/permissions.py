# grouping import
from rest_framework.permissions import (
    AllowAny as AllowAnyPermission,
    IsAuthenticated as IsAuthenticatedPermission,
    IsAdminUser as IsAdminUserPermission,
)
from rest_framework.permissions import BasePermission

from utils.base_errors import BaseErrors
