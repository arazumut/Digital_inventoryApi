from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .models import Item
from .serializers import ItemSerializer, ItemDetailSerializer
from users.permissions import IsAdminUser


class ItemViewSet(viewsets.ModelViewSet):
    """Demirbaş işlemleri için viewset."""
    
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'category', 'assigned_to']
    search_fields = ['name', 'serial_number', 'notes']
    ordering_fields = ['name', 'purchase_date', 'status']
    
    def get_serializer_class(self):
        """
        Liste için ItemSerializer, detay için ItemDetailSerializer.
        """
        if self.action in ['retrieve', 'update', 'partial_update']:
            return ItemDetailSerializer
        return ItemSerializer
    
    def get_permissions(self):
        """
        GET istekleri için herkes, diğer işlemler için sadece admin.
        """
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated, IsAdminUser]
        return [permission() for permission in permission_classes]
    
    @extend_schema(
        summary="Demirbaş listesini getir",
        description="Tüm demirbaşları listeler. Filtreleme desteklenir.",
        parameters=[
            OpenApiParameter(name='status', description='Durum filtresi', required=False, type=str),
            OpenApiParameter(name='category', description='Kategori ID filtresi', required=False, type=int),
            OpenApiParameter(name='assigned_to', description='Atanan kullanıcı ID filtresi', required=False, type=int),
        ],
        responses={200: ItemSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @extend_schema(
        summary="Demirbaş detayını getir",
        description="Belirli bir demirbaşın detaylarını getirir.",
        responses={200: ItemDetailSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(
        summary="Yeni demirbaş oluştur",
        description="Yeni bir demirbaş oluşturur. Sadece admin kullanıcılar erişebilir.",
        responses={201: ItemSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @extend_schema(
        summary="Demirbaş güncelle",
        description="Belirli bir demirbaşı günceller. Sadece admin kullanıcılar erişebilir.",
        responses={200: ItemDetailSerializer}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @extend_schema(
        summary="Demirbaş sil",
        description="Belirli bir demirbaşı siler. Sadece admin kullanıcılar erişebilir.",
        responses={204: None}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
