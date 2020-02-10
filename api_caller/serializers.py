from rest_framework import serializers
from .your_models import YourModel

class YourSerializer(serializers.ModelSerializer):

    class Meta:
        model = YourModel
        fields = ['id', 'description', 'updated_at', etc…]
