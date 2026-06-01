from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    LoginView,
    RegisterView,
    LogoutView,
    MeView,
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
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', MeView.as_view(), name='me'),
    path('', include(router.urls)),
]
