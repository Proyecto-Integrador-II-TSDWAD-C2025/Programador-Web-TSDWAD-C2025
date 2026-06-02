from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    LoginView,
    RegisterView,
    LogoutView,
    MeView,
    PerfilView,
    MiRutinaView,
    CompletarEjercicioView,
    MiPlanAlimenticioView,
    CompletarComidaPlanView,
    RolViewSet,
    UsuarioViewSet,
    PlanViewSet,
    ComidaViewSet,
    UsuarioPlanViewSet,
    PlanComidaViewSet,
    HistorialPesoViewSet,
)

router = DefaultRouter()
router.register(r'roles', RolViewSet)
router.register(r'usuarios', UsuarioViewSet)
router.register(r'planes', PlanViewSet)
router.register(r'comidas', ComidaViewSet)
router.register(r'usuario-planes', UsuarioPlanViewSet)
router.register(r'plan-comidas', PlanComidaViewSet)
router.register(r'historial-peso', HistorialPesoViewSet, basename='historial-peso')

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', MeView.as_view(), name='me'),
    path('perfil/', PerfilView.as_view(), name='perfil'),
    path('mi-rutina/', MiRutinaView.as_view(), name='mi-rutina'),
    path('mi-rutina/completar-ejercicio/', CompletarEjercicioView.as_view(), name='completar-ejercicio'),
    path('mi-plan-alimenticio/', MiPlanAlimenticioView.as_view(), name='mi-plan-alimenticio'),
    path('mi-plan-alimenticio/completar-comida/', CompletarComidaPlanView.as_view(), name='completar-comida-plan'),
    path('', include(router.urls)),
]
