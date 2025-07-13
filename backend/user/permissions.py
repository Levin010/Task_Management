from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """
    Permission class to check if user has admin role
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"


class IsAdminOrReadOnly(BasePermission):
    """
    Permission class to allow read-only access to all users but write access only to admins
    """

    def has_permission(self, request, view):
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.role == "admin"


class IsOwnerOrAdmin(BasePermission):
    """
    Permission class to allow access to resource owner or admin
    """

    def has_object_permission(self, request, view, obj):
        # Admin can access any object
        if request.user.role == "admin":
            return True

        # Users can only access their own objects
        if hasattr(obj, "user"):
            return obj.user == request.user

        # If the object is a User instance, check if it's the same user
        if hasattr(obj, "id") and hasattr(request.user, "id"):
            return obj.id == request.user.id

        return False
