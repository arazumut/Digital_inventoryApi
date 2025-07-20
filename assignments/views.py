from django.shortcuts import render
from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db import transaction
from drf_spectacular.utils import extend_schema, OpenApiResponse
from .models import Assignment
from .serializers import AssignmentSerializer, AssignmentDetailSerializer, AssignmentReturnSerializer
from items.models import Item
from users.permissions import IsAdminUser


class AssignmentViewSet(viewsets.ModelViewSet):
    """Atama işlemleri için viewset."""
    
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    
    def get_serializer_class(self):
        """
        Liste için AssignmentSerializer, detay için AssignmentDetailSerializer.
        """
        if self.action in ['retrieve']:
            return AssignmentDetailSerializer
        return AssignmentSerializer
    
    def get_permissions(self):
        """
        Tüm işlemler için admin yetkisi gerekir.
        """
        return [permissions.IsAuthenticated(), IsAdminUser()]
    
    @extend_schema(
        summary="Atama listesini getir",
        description="Tüm atamaları listeler.",
        responses={200: AssignmentSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @extend_schema(
        summary="Atama detayını getir",
        description="Belirli bir atama kaydının detaylarını getirir.",
        responses={200: AssignmentDetailSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(
        summary="Yeni atama oluştur",
        description="Yeni bir atama kaydı oluşturur. Sadece admin kullanıcılar erişebilir.",
        responses={
            201: AssignmentSerializer,
            400: OpenApiResponse(description="Atama yapılamadı. Demirbaş zaten atanmış olabilir.")
        }
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        item = serializer.validated_data['item']
        
        # İş kuralı: Aynı demirbaş birden fazla kullanıcıya atanamaz
        if item.status == 'assigned':
            return Response(
                {"error": "Bu demirbaş zaten bir kullanıcıya atanmış."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        with transaction.atomic():
            # Demirbaşın durumunu güncelle
            item.status = 'assigned'
            item.assigned_to = serializer.validated_data['assigned_to']
            item.save()
            
            # Atama kaydını oluştur
            self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    @extend_schema(
        summary="Atamayı iade et",
        description="Belirli bir atama kaydını iade işlemi yapar.",
        request=AssignmentReturnSerializer,
        responses={
            200: AssignmentDetailSerializer,
            400: OpenApiResponse(description="İade yapılamadı. Demirbaş zaten iade edilmiş olabilir.")
        }
    )
    @action(detail=True, methods=['patch'], url_path='return')
    def return_item(self, request, pk=None):
        assignment = self.get_object()
        
        # İade edilmiş mi kontrol et
        if assignment.returned_at:
            return Response(
                {"error": "Bu demirbaş zaten iade edilmiş."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = AssignmentReturnSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        with transaction.atomic():
            # Atama kaydını güncelle
            assignment.returned_at = serializer.validated_data.get('returned_at', timezone.now())
            assignment.condition_on_return = serializer.validated_data.get('condition_on_return', '')
            assignment.save()
            
            # Demirbaşın durumunu güncelle
            item = assignment.item
            item.status = 'available'
            item.assigned_to = None
            item.save()
        
        return Response(AssignmentDetailSerializer(assignment).data)
