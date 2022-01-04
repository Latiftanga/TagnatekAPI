from core.permissions import IsStaff
from core.views import CRUDViewSets
from gradebook import serializers, models


class YearViewSets(CRUDViewSets):
    '''Academic Year Viewsets'''
    queryset = models.Year.objects.all()
    serializer_class = serializers.YearSerializer
    permission_classes = (IsStaff, )


class SubjectViewSets(CRUDViewSets):
    '''Subject Viewsets'''
    queryset = models.Subject.objects.all()
    serializer_class = serializers.SubjectSerializer
    permission_classes = (IsStaff, )

    def get_queryset(self):
        return self.queryset


class ClassViewSets(CRUDViewSets):
    '''Class Viewsets'''
    queryset = models.Class.objects.all()
    serializer_class = serializers.ClassSerializer
    permission_classes = (IsStaff, )

    def get_queryset(self):
        return self.queryset
