from rest_framework.permissions import BasePermission
class IsDoctorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user.role == "DOCTOR"
