from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from students.serializers import StudentSerializer
from core.permissions import IsStaff
from core.views import CRUDViewSets
from students.models import Programme, Class, House, Student
from students.serializers import ProgrammeSerializer, \
    ClassSerializer, HouseSerializer, GuaridianSerializer


class ProgrammeViewSets(CRUDViewSets):
    '''Student programmes viewsets'''

    queryset = Programme.objects.all()
    serializer_class = ProgrammeSerializer
    permission_classes = [IsStaff]


class ClassViewSets(CRUDViewSets):
    '''Student classes viewsets'''

    queryset = Class.objects.all()
    serializer_class = ClassSerializer
    permission_classes = [IsStaff]

    def get_queryset(self):
        return self.queryset


class HouseViewSets(CRUDViewSets):
    '''Students houses viewsets'''

    queryset = House.objects.all()
    serializer_class = HouseSerializer
    permission_classes = [IsStaff]


class StudentsViewSets(CRUDViewSets):
    '''Students viewsets'''

    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [IsStaff]

    def get_serializer_class(self):
        """Return appropriate serializer class"""
        if self.action == 'guardians'\
                or self.action == 'guardian_detail':
            return GuaridianSerializer
        return self.serializer_class

    @action(methods=['GET', 'POST'], detail=True, url_path='guardians')
    def guardians(self, request, pk=None):
        student = self.get_object()
        if request.method == 'GET':
            serializer = GuaridianSerializer(
                student.guardians.all(), many=True
                )
            return Response(serializer.data)
        if request.method == 'POST':
            serializer = GuaridianSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                guardian = serializer.save(
                    created_by=self.request.user.email,
                    )
                student.guardians.add(guardian)
                student.save()
                return Response(GuaridianSerializer(guardian).data)
            else:
                return Response(data=None, status=status.HPP_400_BAD_REQUEST)

    @action(
        methods=['GET', 'PUT', 'DELET'],
        url_path='guardians/(?P<g_id>[^/.]+)',
        url_name='guardian_detail', detail=True
        )
    def guardian_detail(self, request, g_id, pk=None):
        student = self.get_object()
        guardian = student.guardians.filter(id=g_id).first()
        if guardian:
            if request.method == 'GET':
                return Response(GuaridianSerializer(guardian).data)
            if request.method == 'PUT':
                serializer = GuaridianSerializer(guardian, request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save(
                    updated_by=request.user.email
                    )
                return Response(serializer.data)
            if request.method == 'DELETE':
                guardian.delete()
                return Response(data=None, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                {'detail': 'Not found'},
                status=status.HTTP_404_NOT_FOUND
                )
