from rest_framework.authentication import TokenAuthentication
from djforge_redis_multitokens.tokens_auth import MultiToken
from django.contrib.auth import get_user_model
from rest_framework import exceptions
from django.conf import settings


class CachedTokenAuthentication(TokenAuthentication):
    keyword = 'Authorization'

    def authenticate_credentials(self, key):
        try:
            user = MultiToken.get_user_from_token(key)

            if settings.DJFORGE_REDIS_MULTITOKENS.get('RESET_TOKEN_TTL_ON_USER_LOG_IN'):
                MultiToken.reset_tokens_ttl(user.pk)

        except get_user_model().DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token.')

        if not user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted.')

        return (user, MultiToken(key, user))
