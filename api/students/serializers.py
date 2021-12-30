from rest_framework.serializers import ModelSerializer
from students.models import Programme


class ProgrammeSerializer(ModelSerializer):
    '''Programme model serializer'''

    class Meta:
        model = Programme
        fields = '__all__'
        read_only_fields = (
            'id',
            'created',
            'created_by',
            'updated',
            'updated_by'
            )
