from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db import connection

from .models import Rol, Usuario, Plan, Comida, UsuarioPlan, PlanComida
from .serializers import (
    RolSerializer,
    UsuarioSerializer, UsuarioReadSerializer,
    PlanSerializer,
    ComidaSerializer,
    UsuarioPlanSerializer, UsuarioPlanReadSerializer,
    PlanComidaSerializer, PlanComidaReadSerializer,
)


class LoginView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UsuarioReadSerializer

    def post(self, request):
        email = request.data.get('email')
        contrasena = request.data.get('contrasena')

        if not email or not contrasena:
            return Response(
                {'error': 'Email y contraseña son requeridos'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            usuario = Usuario.objects.select_related('id_rol').get(email=email, contrasena=contrasena)
            serializer = UsuarioReadSerializer(usuario)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Usuario.DoesNotExist:
            return Response(
                {'error': 'Credenciales inválidas'},
                status=status.HTTP_401_UNAUTHORIZED
            )


class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.all()
    serializer_class = RolSerializer
    permission_classes = [AllowAny]


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.select_related('id_rol').all()
    serializer_class = UsuarioSerializer
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return UsuarioReadSerializer
        return UsuarioSerializer

    @action(detail=False, methods=['get'])
    def test(self, request):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            return Response({
                'status': 'success',
                'message': 'Conexión con la base de datos MySQL exitosa',
                'info': 'NutriApp - Backend API',
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.all()
    serializer_class = PlanSerializer
    permission_classes = [AllowAny]


class ComidaViewSet(viewsets.ModelViewSet):
    queryset = Comida.objects.all()
    serializer_class = ComidaSerializer
    permission_classes = [AllowAny]


class UsuarioPlanViewSet(viewsets.ModelViewSet):
    queryset = UsuarioPlan.objects.select_related('id_usuario', 'id_plan').all()
    serializer_class = UsuarioPlanSerializer
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return UsuarioPlanReadSerializer
        return UsuarioPlanSerializer

    @action(detail=False, methods=['get'], url_path='por-usuario/(?P<usuario_id>[^/.]+)')
    def por_usuario(self, request, usuario_id=None):
        planes = self.queryset.filter(id_usuario=usuario_id)
        serializer = UsuarioPlanReadSerializer(planes, many=True)
        return Response(serializer.data)


class PlanComidaViewSet(viewsets.ModelViewSet):
    queryset = PlanComida.objects.select_related('id_plan', 'id_comida').all()
    serializer_class = PlanComidaSerializer
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return PlanComidaReadSerializer
        return PlanComidaSerializer

    @action(detail=False, methods=['get'], url_path='por-plan/(?P<plan_id>[^/.]+)')
    def por_plan(self, request, plan_id=None):
        comidas = self.queryset.filter(id_plan=plan_id)
        serializer = PlanComidaReadSerializer(comidas, many=True)
        return Response(serializer.data)
