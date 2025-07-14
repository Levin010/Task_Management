from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import UntypedToken
from django.contrib.auth.models import AnonymousUser


class CookieJWTAuthentication(JWTAuthentication):
    """
    Custom JWT authentication that reads tokens from HTTP-only cookies
    instead of the Authorization header.
    """

    def authenticate(self, request):
        # Try to get the access token from cookies
        raw_token = request.COOKIES.get("access_token")

        if raw_token is None:
            return None

        # Validate the token
        validated_token = self.get_validated_token(raw_token)
        user = self.get_user(validated_token)

        return (user, validated_token)

    def get_validated_token(self, raw_token):
        """
        Validates an encoded JSON Web Token and returns a validated token
        wrapper object.
        """
        messages = []
        for AuthToken in self.get_jti_claim_types():
            try:
                return AuthToken(raw_token)
            except TokenError as e:
                messages.append(
                    {
                        "token_class": AuthToken.__name__,
                        "token_type": AuthToken.token_type,
                        "message": e.args[0],
                    }
                )

        raise InvalidToken(
            {
                "detail": "Given token not valid for any token type",
                "messages": messages,
            }
        )
