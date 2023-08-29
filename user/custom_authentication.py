import jwt
from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed, ParseError

from atm.settings import SECRET_KEY
from user.models import User


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # Extract the JWT from the Authorization header
        jwt_token = request.META.get('HTTP_AUTHORIZATION')
        if jwt_token is None:
            return None

        jwt_token = JWTAuthentication.get_the_token_from_header(jwt_token)  # clean the token
        # Decode the JWT and verify its signature
        try:
            payload = jwt.decode(jwt_token, key=SECRET_KEY, algorithms=['HS256'])
        except jwt.exceptions.InvalidSignatureError:
            raise AuthenticationFailed('Invalid signature')


        user_id = payload.get('user_id')

        if user_id is None:
            raise AuthenticationFailed('User identifier not found in JWT')

        user = User.objects.filter(id=user_id).first()
        if user is None:
            raise AuthenticationFailed('User not found')

        # Return the user and token payload

        return user, payload

    @classmethod
    def get_the_token_from_header(cls, token):
        token = token.replace('Bearer', '').replace(' ', '')  # clean the token
        return token
