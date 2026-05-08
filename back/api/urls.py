from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    LoginView,
    RolViewSet,
    UsuarioViewSet,
    PlanViewSet,
    ComidaViewSet,
    UsuarioPlanViewSet,
    PlanComidaViewSet,
)

router = DefaultRouter()
router.register(r'roles', RolViewSet)
router.register(r'usuarios', UsuarioViewSet)
router.register(r'planes', PlanViewSet)
router.register(r'comidas', ComidaViewSet)
router.register(r'usuario-planes', UsuarioPlanViewSet)
router.register(r'plan-comidas', PlanComidaViewSet)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('', include(router.urls)),
]
