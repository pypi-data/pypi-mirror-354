from rest_framework import parsers, renderers, status

from garpix_user.models.access_token import AccessToken as Token
from garpix_user.serializers.refresh_token_serializer import RefreshTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from garpix_user.models.refresh_token import RefreshToken
from django.utils import timezone
from datetime import timedelta

from garpix_user.utils.get_password_settings import get_password_settings


class RefreshTokenView(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = RefreshTokenSerializer

    def post(self, request, *args, **kwargs):
        refresh_token_ttl_seconds = get_password_settings()['refresh_token_ttl_seconds']
        access_token_ttl_seconds = get_password_settings()['access_token_ttl_seconds']
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        refresh_token = serializer.validated_data['refresh_token']
        try:
            refresh_token_obj = RefreshToken.objects.get(key=refresh_token)
            if refresh_token_ttl_seconds > 0:
                if refresh_token_obj.created + timedelta(seconds=refresh_token_ttl_seconds) < timezone.now():
                    refresh_token_obj.delete()
                    raise Exception("Token expired.")
            token = Token.objects.create(user=refresh_token_obj.user)
            return Response({
                'access_token': token.key,
                'access_token_expires': access_token_ttl_seconds,
                'result': True,
            })
        except:  # noqa
            return Response({'result': False}, status=status.HTTP_400_BAD_REQUEST)


refresh_token_view = RefreshTokenView.as_view()
