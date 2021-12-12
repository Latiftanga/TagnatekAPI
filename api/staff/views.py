from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.permissions import StaffPermission
from core.authentication import JWTAuthentication

from staff.models import (
    Qualification,
    Department,
    Staff
    )

from staff.serializers import (
    DepartmentSerializer,
    QualificationSerializer,
    StaffSerializer
    )


class BaseStaffAttrViewSet(
        viewsets.GenericViewSet,
        mixins.ListModelMixin,
        mixins.CreateModelMixin
        ):
    """Base viewset for user owned recipe attributes"""
    authentication_classes = (
        TokenAuthentication,
        JWTAuthentication
        )
    permission_classes = (IsAuthenticated,)

    # def get_queryset(self):
    #     assigned_only = bool(self.request.query_params.get('assigned_only'))
    #     queryset = self.queryset

    #     if assigned_only:
    #         queryset = queryset.filter(recipe__isnull=False)

    #     return queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save()


class DepartmentViewSets(BaseStaffAttrViewSet):
    """Manage tags in the database"""
    permission_classes = (StaffPermission,)
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class QualificationViewSets(BaseStaffAttrViewSet):
    """Manage ingredients in the database"""
    queryset = Qualification.objects.all()
    serializer_class = QualificationSerializer


class StaffViewSetAPIView(viewsets.ModelViewSet):
    """Manage recipes in the database"""
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer

    authentication_classes = (TokenAuthentication,)
    permission_classes = (StaffPermission,)

    def _params_to_ints(self, qs):
        """Convert a list of string IDs to a list integers"""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Retrieve recipe for authenticated user"""
        tags = self.request.query_params.get('tags')
        ingredients = self.request.query_params.get('ingredients')
        queryset = self.queryset

        if tags:
            tag_ids = self._params_to_ints(tags)
            queryset = queryset.filter(tags__id__in=tag_ids)

        if ingredients:
            ingredient_ids = self._params_to_ints(ingredients)
            queryset = queryset.filter(ingredients__id__in=ingredient_ids)

        return queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return StaffSerializer
        elif self.action == 'upload_image':
            return 'RecipeImageSerializer'

        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
