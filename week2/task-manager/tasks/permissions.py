from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return ( request.user.is_staff or obj.owner_id == request.user.id )