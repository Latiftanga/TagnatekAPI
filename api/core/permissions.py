from rest_framework.permissions import BasePermission


class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff


class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return request.user.role.name == 'teacher'


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return request.user.role.name == 'student'


class IsParent(BasePermission):
    def has_permission(self, request, view):
        return request.user.role.name == 'parent'


class StaffPermission(BasePermission):
    '''Custom permission for staff model'''

    def has_permission(self, request, view):
        user = request.user
        if view.action == 'create' or view.action == 'list' \
                or view.action == 'update' or view.action == 'destroy':
            return user.is_staff or user.role.name == 'admin'
        elif view.action == 'retrieve':
            return user.is_staff or user.role.name == 'teacher' \
                or user.role.name == 'admin'
        return False
