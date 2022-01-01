from students.serializers import StudentSerializer
from core.permissions import IsStaff
from core.views import CRUDViewSets
from students.models import Programme, Class, House, Student
from students.serializers import ProgrammeSerializer, \
                                ClassSerializer, HouseSerializer


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
