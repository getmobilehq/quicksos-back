from rest_framework import serializers
from .models import AssignedCase, Report


class AssignedCaseSerializer(serializers.ModelSerializer):
    case_detail = serializers.ReadOnlyField()
    issue = serializers.ReadOnlyField()
    img_url = serializers.ReadOnlyField()
    
    class Meta:
        model = AssignedCase
        fields = '__all__'
        
        
class ReportSerializer(serializers.ModelSerializer):
    img1 = serializers.ImageField()
    img2 = serializers.ImageField(required=False)
    mark_complete = serializers.BooleanField()
    
    class Meta:
        model=Report
        fields = '__all__'