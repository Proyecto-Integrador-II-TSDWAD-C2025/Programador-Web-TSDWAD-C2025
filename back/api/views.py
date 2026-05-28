from django.db import connection
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Comida, Plan, PlanComida, Rol, Usuario, UsuarioPlan
from .permissions import (
    IsAdminOrNutritionistRole,
    IsAdminRole,
    IsAuthenticatedReadOrStaffRoleWrite,
    IsSelfOrAdminRole,
    user_has_role,
)
from .serializers import (
    ComidaSerializer,
    LoginSerializer,
    PlanComidaReadSerializer,
    PlanComidaSerializer,
    PlanSerializer,
    RolSerializer,
    UsuarioPlanReadSerializer,
    UsuarioPlanSerializer,
    UsuarioReadSerializer,
    UsuarioSerializer,
)


class LoginView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        usuario = serializer.validated_data['usuario']
        token, _ = Token.objects.get_or_create(user=usuario)

        return Response({
            'token': token.key,
            'usuario': UsuarioReadSerializer(usuario).data,
        }, status=status.HTTP_200_OK)


class RolViewSet(viewsets.ModelViewSet):
    queryset = Rol.objects.order_by('id_rol')
    serializer_class = RolSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]

        return [IsAdminRole()]


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.select_related('id_rol').order_by('id_usuario')
    serializer_class = UsuarioSerializer

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return UsuarioReadSerializer

        return UsuarioSerializer

    def get_permissions(self):
        if self.action in ['create', 'test']:
            return [AllowAny()]
        if self.action in ['list', 'destroy']:
            return [IsAdminRole()]
        if self.action in ['retrieve', 'update', 'partial_update']:
            return [IsAuthenticated(), IsSelfOrAdminRole()]

        return [IsAuthenticated()]

    @action(detail=False, methods=['get'])
    def test(self, request):
        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT 1')
            return Response({
                'status': 'success',
                'message': 'Conexion con la base de datos MySQL exitosa',
                'info': 'NutriApp - Backend API',
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PlanViewSet(viewsets.ModelViewSet):
    queryset = Plan.objects.order_by('id_plan')
    serializer_class = PlanSerializer
    permission_classes = [IsAuthenticatedReadOrStaffRoleWrite]


class ComidaViewSet(viewsets.ModelViewSet):
    queryset = Comida.objects.order_by('id_comida')
    serializer_class = ComidaSerializer
    permission_classes = [IsAuthenticatedReadOrStaffRoleWrite]


class UsuarioPlanViewSet(viewsets.ModelViewSet):
    queryset = UsuarioPlan.objects.select_related('id_usuario', 'id_plan').order_by('id_usuario_plan')
    serializer_class = UsuarioPlanSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        if user_has_role(self.request.user, 'administrador', 'nutricionista'):
            return queryset

        return queryset.filter(id_usuario=self.request.user)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return UsuarioPlanReadSerializer

        return UsuarioPlanSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminOrNutritionistRole()]

        return [IsAuthenticated()]

    @action(detail=False, methods=['get'], url_path='por-usuario/(?P<usuario_id>[^/.]+)')
    def por_usuario(self, request, usuario_id=None):
        if not user_has_role(request.user, 'administrador', 'nutricionista'):
            usuario_id = request.user.id_usuario

        planes = self.get_queryset().filter(id_usuario=usuario_id)
        serializer = UsuarioPlanReadSerializer(planes, many=True)
        return Response(serializer.data)


class PlanComidaViewSet(viewsets.ModelViewSet):
    queryset = PlanComida.objects.select_related('id_plan', 'id_comida').order_by('id_plan_comida')
    serializer_class = PlanComidaSerializer
    permission_classes = [IsAuthenticatedReadOrStaffRoleWrite]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return PlanComidaReadSerializer

        return PlanComidaSerializer

    @action(detail=False, methods=['get'], url_path='por-plan/(?P<plan_id>[^/.]+)')
    def por_plan(self, request, plan_id=None):
        comidas = self.queryset.filter(id_plan=plan_id)
        serializer = PlanComidaReadSerializer(comidas, many=True)
        return Response(serializer.data)
