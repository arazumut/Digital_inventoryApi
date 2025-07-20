from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login, logout
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema, OpenApiResponse
from .serializers import UserSerializer, UserDetailSerializer, RegisterSerializer, LoginSerializer
from .models import User
from .permissions import IsAdminUser


class RegisterView(generics.CreateAPIView):
    """Kullanıcı kaydı için view."""
    
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    serializer_class = RegisterSerializer
    
    @extend_schema(
        summary="Yeni kullanıcı oluştur",
        description="Sadece admin kullanıcılar yeni kullanıcı oluşturabilir.",
        responses={201: OpenApiResponse(description="Kullanıcı başarıyla oluşturuldu")}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class LoginView(APIView):
    """Kullanıcı girişi için view."""
    
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer
    
    @extend_schema(
        summary="Kullanıcı girişi",
        description="Email ve şifre ile giriş yapar.",
        responses={
            200: OpenApiResponse(description="Başarılı giriş"),
            400: OpenApiResponse(description="Geçersiz kimlik bilgileri")
        }
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = authenticate(
            request,
            username=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )
        
        if user is not None:
            login(request, user)
            return Response({
                "message": _("Giriş başarılı."),
                "user": UserSerializer(user).data
            })
        else:
            return Response(
                {"error": _("Geçersiz email veya şifre.")},
                status=status.HTTP_400_BAD_REQUEST
            )


class LogoutView(APIView):
    """Kullanıcı çıkışı için view."""
    
    permission_classes = [permissions.IsAuthenticated]
    
    @extend_schema(
        summary="Kullanıcı çıkışı",
        description="Mevcut oturumu sonlandırır.",
        responses={200: OpenApiResponse(description="Başarılı çıkış")}
    )
    def post(self, request):
        logout(request)
        return Response({"message": _("Çıkış başarılı.")})


class UserListView(generics.ListAPIView):
    """Kullanıcı listesi için view."""
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    
    @extend_schema(
        summary="Kullanıcı listesini getir",
        description="Sadece admin kullanıcılar tüm kullanıcıları listeleyebilir.",
        responses={200: UserSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """Kullanıcı profili için view."""
    
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @extend_schema(
        summary="Kullanıcı profilini getir",
        description="Giriş yapmış kullanıcının kendi profilini getirir.",
        responses={200: UserDetailSerializer}
    )
    def get_object(self):
        return self.request.user
