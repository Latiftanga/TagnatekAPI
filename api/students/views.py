from core.permissions import IsStaff
from core.views import CRUDViewSets
from students.models import Programme
from students.serializers import ProgrammeSerializer


class ProgrammeViewSets(CRUDViewSets):
    '''Student programmes viewsets'''

    queryset = Programme.objects.all()
    serializer_class = ProgrammeSerializer
    permission_classes = [IsStaff]

    def get_queryset(self):
        return self.queryset
