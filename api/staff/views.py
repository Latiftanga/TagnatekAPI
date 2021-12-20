from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from staff.models import Qualification
from core.models import Role
from core.permissions import IsStaff
from core.serializers import UserSerializer
from core.authentication import JWTAuthentication


from staff.models import (
    Department,
    Staff
    )

from staff.serializers import (
    DepartmentSerializer,
    QualificationSerializer,
    StaffSerializer,
    StaffDetailSerializer,
    PromotionSerializer
    )


class DepartmentViewSets(viewsets.ModelViewSet):
    """Manage tags in the database"""
    authentication_classes = (
        JWTAuthentication,
        TokenAuthentication
        )
    permission_classes = (
        IsStaff,
        )
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class StaffViewSets(
        viewsets.GenericViewSet,
        mixins.ListModelMixin,
        mixins.CreateModelMixin,
        mixins.UpdateModelMixin,
        mixins.RetrieveModelMixin
        ):
    """Manage recipes in the database"""
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer

    authentication_classes = (
        JWTAuthentication,
        TokenAuthentication
        )
    permission_classes = (IsStaff,)

    def perform_create(self, serializer):
        """Create a new object"""
        serializer.save(
            school=self.request.user.school,
            created_by=self.request.user.email
            )

    def _params_to_ints(self, qs):
        """Convert a list of string IDs to a list integers"""
        return [int(str_id) for str_id in qs.split(',')]

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'retrieve':
            return StaffDetailSerializer
        if self.action == 'qualifications' \
                or self.action == 'qualification_detail':
            return QualificationSerializer
        if self.action == 'account':
            return UserSerializer
        if self.action == 'appointments'\
                or self.action == 'appointment_detail':
            return PromotionSerializer
        if self.action == 'promotions'\
                or self.action == 'promotion_detail':
            return PromotionSerializer
        return self.serializer_class

    def get_queryset(self):
        return self.queryset.filter(
            school=self.request.user.school
            ).order_by('first_name')

    def perform_update(self, serializer):
        return serializer.save(
            updated_by=self.request.user.email
            )

    @action(
        methods=['GET', 'POST'],
        detail=True,
        url_path='qualifications',
        url_name='staff_qualifications'
        )
    def qualifications(self, request, pk=None):
        staff = self.get_object()
        if request.method == 'GET':
            serializer = QualificationSerializer(
                staff.qualifications.all(),
                many=True
                )
            return Response(serializer.data)
        if request.method == 'POST':
            serializer = QualificationSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(
                    created_by=request.user.email,
                    staff=staff
                    )
                return Response(serializer.data)
        return Response(data=None, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(
        methods=['GET', 'PUT', 'DELETE'],
        detail=True,
        url_path='qualifications/(?P<q_id>[^/.]+)',
        url_name='qualification_detail'
        )
    def qualification_detail(self, request, q_id, pk=None):
        staff = self.get_object()

        if request.method == 'GET':
            qs = staff.qualifications.filter(id=q_id).first()
            serializer = QualificationSerializer(qs)
            return Response(serializer.data)
        if request.method == 'PUT':
            instance = Qualification.objects.get(id=q_id)
            serializer = QualificationSerializer(
                instance, request.data
                )
            if serializer.is_valid():
                serializer.save(updated_by=request.user.email)
                return Response(serializer.data)
        if request.method == 'DELETE':
            qualification = Qualification.objects.get(id=q_id)
            qualification.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['GET', 'POST'], detail=True, url_path='account')
    def account(self, request, pk=None):
        staff = self.get_object()
        if request.method == 'GET':
            if staff.user:
                return UserSerializer((staff.user).data)
            return Response({'message': f'{str(staff)} has no account'})
        if request.method == 'POST':
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                role = Role.objects.get(name='teacher')
                user = serializer.save(
                    created_by=request.user.email,
                    role=role.id,
                    school=request.user.school
                    )
                staff.user = user
                staff.save()
                return Response(UserSerializer(user).data)
        return Response(data=None, status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=['GET', 'POST'],
        detail=True,
        url_path='appointments',
        url_name='appointments'
        )
    def appointments(self, request, pk=None):
        '''Staff appontments '''
        staff = self.get_object()
        if request.method == 'GET':
            appointments = staff.appointments.all()
            serializer = PromotionSerializer(appointments, many=True)
            return Response(serializer.data)
        if request.method == 'POST':
            print(request.data)
            serializer = PromotionSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            job = serializer.save(
                staff=staff,
                created_by=request.user.email,
                )
            staff.save()
            return Response(PromotionSerializer(job).data)
        return Response(data=None, status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=['GET', 'PUT', 'DELETE'],
        detail=True,
        url_path='appointments/(?P<a_id>[^/.]+)',
        url_name='appointment_detail'
        )
    def appointement_detail(self, request, a_id, pk=None):
        '''viewing and updating appointment'''
        staff = self.get_object()
        appointment = staff.appointments.filter(id=a_id).first()
        if appointment:
            if request.method == 'GET':
                return Response(PromotionSerializer(appointment).data)
            if request.method == 'PUT':
                serializer = PromotionSerializer(appointment, request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save(
                    updated_by=request.user.email
                    )
                return Response(serializer.data)
            if request.method == 'DELETE':
                appointment.delete()
                return Response(data=None, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(data=None, status=status.HTTP_404_NOT_FOUND)

    @action(
        methods=['GET', 'POST'],
        detail=True,
        url_path='promotions',
        url_name='promotions'
        )
    def promotions(self, request, pk=None):
        '''Staff promotion'''
        staff = self.get_object()

        if request.method =='GET':
            promotions = staff.promotions.all()
            serializer = PromotionSerializer(promotions, many=True)
            return Response(serializer.data)
        if request.method == 'POST':
            serializer = PromotionSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(
                    created_by=request.user.email,
                    staff=staff,
                    )
            return Response(serializer.data)
        return Response(
            {'message': 'Method not allowed'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
            )

    @action(
        methods=['GET', 'PUT', 'DELETE'],
        detail=True,
        url_path='promotions/(?P<p_id>[^/.]+)',
        url_name='promotion_detail'
        )
    def promotion_detail(self, request, p_id, pk=None):
        '''viewing and updating promotions'''
        staff = self.get_object()
        promotion = staff.promotions.filter(id=p_id).first()
        if promotion:
            if request.method == 'GET':
                return Response(PromotionSerializer(promotion).data)
            if request.method == 'PUT':
                serializer = PromotionSerializer(promotion, request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save(
                    updated_by=request.user.email
                    )
                return Response(serializer.data)
            if request.method == 'DELETE':
                promotion.delete()
                return Response(data=None, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(data=None, status=status.HTTP_404_NOT_FOUND)
