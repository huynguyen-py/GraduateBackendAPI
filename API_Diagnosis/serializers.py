from rest_framework import serializers
from .models import DiagnosisRecord


class DiagnosisRecordSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username', read_only=True)
    class Meta:
        model = DiagnosisRecord
        fields = ['id', 'author', 'create_at', 'image_record',
                  'gender', 'anatom_site_general_challenge', 'age_approx']
        read_only_fields = ['id']
        extra_kwargs = {
            'anatom_site_general_challenge': {
                'required': True,
            },
            'gender': {
                'required': True,
            },
            'age_approx': {
                'required': True,
            },
        }
