from rest_framework_jwt.authentication import BaseAuthentication, jwt_decode_handler
import jwt
from rest_framework import exceptions

class JWTAuthentication(BaseAuthentication):
    def authenticate(self,request):
        jwt_token = request.META.get("HTTP_AUTHORIZATION")

        token = self.parse_jwt_token(jwt_token)

        if token is None:
            return None

        try:
            payload = jwt_decode_handler(token)
        except jwt.ExpiredSignature:
            raise exceptions.AuthenticationFailed("签名失效")
        except:
            raise exceptions.AuthenticationFailed("无效签名")
        user = self.authenticate_credentials(payload)

        return user,token

    def parse_jwt_token(self,jwt_token):
        tokens = jwt_token.split()
        if len(tokens) != 3 or tokens[0].lower() != "jwt":
            return None
        return tokens[1]