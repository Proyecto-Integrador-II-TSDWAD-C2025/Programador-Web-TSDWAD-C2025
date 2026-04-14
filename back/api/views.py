from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Usuario
from .serializers import UsuarioSerializer


class UsuarioViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar Usuarios"""
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    
    @action(detail=False, methods=['get'])
    def test(self, request):
        """Endpoint de prueba para evaluar la conexión con la base de datos"""
        try:
            usuario_count = Usuario.objects.count()
            return Response({
                'status': 'success',
                'message': 'Conexión con la base de datos MySQL exitosa',
                'usuarios_totales': usuario_count,
                'info': 'ProyectoIntegrador - Backend API'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
