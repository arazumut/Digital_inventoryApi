from rest_framework import serializers
from .models import Item
from categories.serializers import CategorySerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class UserMinimalSerializer(serializers.ModelSerializer):
    """User model için minimal serializer."""
    
    class Meta:
        model = User
        fields = ['id', 'email', 'full_name']


class ItemSerializer(serializers.ModelSerializer):
    """Item model için serializer."""
    
    class Meta:
        model = Item
        fields = [
            'id', 'name', 'serial_number', 'category', 'assigned_to', 
            'status', 'purchase_date', 'warranty_until', 'notes', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ItemDetailSerializer(serializers.ModelSerializer):
    """Item model için detaylı serializer."""
    
    category = CategorySerializer(read_only=True)
    assigned_to = UserMinimalSerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        write_only=True, 
        queryset=Item.objects.all(),
        source='category'
    )
    
    class Meta:
        model = Item
        fields = [
            'id', 'name', 'serial_number', 'category', 'category_id',
            'assigned_to', 'status', 'purchase_date', 'warranty_until', 
            'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at'] 