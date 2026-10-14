"""Tokens DRF con vencimiento absoluto, compatibles con el cliente Android."""

from datetime import timedelta

from django.conf import settings
from django.db import transaction
from django.utils import timezone
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

from .models import Usuario


def token_expires_at(token):
    return token.created + timedelta(minutes=settings.AUTH_TOKEN_TTL_MINUTES)


def token_is_expired(token):
    return timezone.now() >= token_expires_at(token)


def issue_token_for_user(user):
    # Serializa logins de la misma cuenta en MySQL. No rota sesiones vigentes
    # ni extiende su plazo cuando otra persona entra con la cuenta compartida.
    with transaction.atomic():
        Usuario.objects.select_for_update().get(pk=user.pk)
        token, _ = Token.objects.get_or_create(user=user)
        if token_is_expired(token):
            token.delete()
            token = Token.objects.create(user=user)
        return token


class ExpiringTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        user, token = super().authenticate_credentials(key)
        if token_is_expired(token):
            # No borrar desde una lectura: un login concurrente puede estar
            # reemplazando este token. Un token vencido nunca autoriza la API.
            raise AuthenticationFailed(
                'Tu sesion expiro. Inicia sesion de nuevo.', code='token_expired'
            )
        return user, token
