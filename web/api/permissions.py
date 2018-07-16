from rest_framework import permissions
from api.models import Group


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        try:
            return obj.created_by == request.user or obj.owner == request.user
        except AttributeError:
            return False

class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_admin:
            return True

class IsAdminOrOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        gid = view.kwargs.get('gid') or request.GET.get('gid') or request.data.get('gid')
        if request.method in permissions.SAFE_METHODS and not gid:
            return True
        return Group.objects.filter(id=gid, users__in=[request.user]).first()


class IsGroupAccessable(permissions.BasePermission):

    def has_permission(self, request, view):
        gid = view.kwargs.get('gid') or request.GET.get('gid') or request.data.get('gid')
        if request.method in permissions.SAFE_METHODS and not gid:
            return True
        return Group.objects.filter(id=gid, users__in=[request.user]).first()
