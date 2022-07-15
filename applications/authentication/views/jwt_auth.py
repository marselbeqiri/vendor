from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenViewBase

from applications.authentication import serializers


class TokenObtainPairView(TokenViewBase):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """

    serializer_class = serializers.TokenObtainPairSerializer


custom_token_obtain_pair_view = TokenObtainPairView.as_view()


class TokenRefreshView(TokenViewBase):
    """
    Takes a refresh type JSON web token and returns an access type JSON web
    token if the refresh token is valid.
    """

    serializer_class = serializers.TokenRefreshSerializer


custom_token_refresh_view = TokenRefreshView.as_view()


class LogoutAllView(APIView):
    def post(self, request):
        token_key_lookup = f"token_key_{self.request.user.id}"
        cache.delete(token_key_lookup)

        return Response("Logged out successfully.")


logout_all_view = LogoutAllView.as_view()
