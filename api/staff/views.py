from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from staff.serializers import JobSerializer
from staff.models import Qualification
from core.models import Role
from staff.serializers import QualificationSerializer
from core.permissions import IsStaff
from core.serializers import UserSerializer
from core.authentication import JWTAuthentication


from staff.models import (
    Department,
    Staff
    )

from staff.serializers import (
    DepartmentSerializer,
    StaffSerializer,
    StaffDetailSerializer
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
        if self.action == 'jobs' or self.action == 'job_detail':
            return JobSerializer
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
            if serializer.is_valid():
                serializer.save(staff=staff)
                serializer1 = QualificationSerializer(
                    staff.qualifications.all(),
                    many=True
                    )
                return Response(serializer1.data)
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
            serializer = QualificationSerializer(
                staff.qualifications.filter(id=q_id).first()
                )
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

            serializer = UserSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                role = Role.objects.get(name='teacher')
                user = serializer.save(
                    created_by=request.user.email,
                    role=role.id,
                    school=request.user.school
                    )
                staff.user = user
                staff.save(updated_by=request.user.email)
                return Response(UserSerializer(user).data)
        return Response(data=None, status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=['GET', 'PUT', 'DELETE'],
        detail=True,
        url_path='jobs/(?P<j_id>[^/.]+)',
        url_name='job_detail'
        )
    def jobs(self, request, pk=None):
        '''Staff jobs '''
        staff = self.get_object()
        if request.method == 'GET':
            jobs = staff.jobs.all()
            serializer = JobSerializer(jobs, many=True)
            return Response(serializer.data)
        if request.method == 'POST':
            serializer = JobSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            job = serializer.save(
                created_by=request.user.email,
                )
            staff.jobs.add(job)
            staff.save()
            return Response(JobSerializer(staff.jobs, many=True).data)
        return Response(data=None, status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=['GET', 'PUT', 'DELETE'],
        detail=True,
        url_path='jobs/(?P<j_id>[^/.]+)',
        url_name='job_detail'
        )
    def job_detail(self, request, j_id, pk=None):
        '''viewing and updating job by a particular staff'''
        staff = self.get_object()
        job = staff.jobs.filter(id=j_id).first()
        if job:
            if request.method == 'GET':
                return Response(JobSerializer(job).data)
            if request.method == 'PUT':
                serializer = JobSerializer(job, request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save(
                    updated_by=request.user.email
                    )
                return Response(serializer.data)
            if request.method == 'DELETE':
                job.delete()
                return Response(data=None, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(data=None, status=status.HTTP_404_NOT_FOUND)
