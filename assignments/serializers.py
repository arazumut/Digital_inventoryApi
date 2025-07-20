from rest_framework import serializers
from .models import Assignment
from items.serializers import ItemSerializer, UserMinimalSerializer


class AssignmentSerializer(serializers.ModelSerializer):
    """Assignment model için serializer."""
    
    class Meta:
        model = Assignment
        fields = [
            'id', 'item', 'assigned_to', 'assigned_by', 
            'assigned_at', 'returned_at', 'condition_on_return'
        ]
        read_only_fields = ['id', 'assigned_by', 'assigned_at']
    
    def create(self, validated_data):
        # Atama yapan kişiyi mevcut kullanıcı olarak ayarla
        validated_data['assigned_by'] = self.context['request'].user
        return super().create(validated_data)


class AssignmentDetailSerializer(serializers.ModelSerializer):
    """Assignment model için detaylı serializer."""
    
    item = ItemSerializer(read_only=True)
    assigned_to = UserMinimalSerializer(read_only=True)
    assigned_by = UserMinimalSerializer(read_only=True)
    
    class Meta:
        model = Assignment
        fields = [
            'id', 'item', 'assigned_to', 'assigned_by', 
            'assigned_at', 'returned_at', 'condition_on_return'
        ]
        read_only_fields = ['id', 'assigned_at']


class AssignmentReturnSerializer(serializers.ModelSerializer):
    """Assignment iade işlemi için serializer."""
    
    class Meta:
        model = Assignment
        fields = ['returned_at', 'condition_on_return'] 