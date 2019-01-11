from rest_framework import permissions


class IsPowtoonOwnerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):

        if view.action in ['update', 'destroy']:
            powtoon = view.get_object()
            has_perm = request.user == powtoon.user or request.user.has_perm('api.can_share')
            return has_perm

        return True
