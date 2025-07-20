from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    """Category model için serializer."""
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at'] 