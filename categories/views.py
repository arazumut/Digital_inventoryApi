from django.shortcuts import render
from rest_framework import viewsets, permissions
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .models import Category
from .serializers import CategorySerializer
from users.permissions import IsAdminUser


class CategoryViewSet(viewsets.ModelViewSet):
    """Kategori işlemleri için viewset."""
    
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
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
        summary="Kategori listesini getir",
        description="Tüm kategorileri listeler.",
        responses={200: CategorySerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @extend_schema(
        summary="Kategori detayını getir",
        description="Belirli bir kategorinin detaylarını getirir.",
        responses={200: CategorySerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(
        summary="Yeni kategori oluştur",
        description="Yeni bir kategori oluşturur. Sadece admin kullanıcılar erişebilir.",
        responses={201: CategorySerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    @extend_schema(
        summary="Kategori güncelle",
        description="Belirli bir kategoriyi günceller. Sadece admin kullanıcılar erişebilir.",
        responses={200: CategorySerializer}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @extend_schema(
        summary="Kategori sil",
        description="Belirli bir kategoriyi siler. Sadece admin kullanıcılar erişebilir.",
        responses={204: None}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
