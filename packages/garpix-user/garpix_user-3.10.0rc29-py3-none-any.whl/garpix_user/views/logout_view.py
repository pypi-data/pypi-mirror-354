from garpix_utils.cef_logs.event import LogoutEvent
from rest_framework import parsers, renderers
from garpix_user.models.access_token import AccessToken as Token
from oauth2_provider.models import AccessToken
from rest_framework.response import Response
from rest_framework.views import APIView
from garpix_user.models.refresh_token import RefreshToken
from rest_framework.permissions import IsAuthenticated
from garpix_user.utils import get_token_from_request


class LogoutView(APIView):
    throttle_classes = ()
    permission_classes = (IsAuthenticated,)
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            token = get_token_from_request(request)
            if token is not None:
                Token.objects.filter(key=token).delete()
                AccessToken.objects.filter(token=token).delete()
                RefreshToken.objects.filter(key=token).delete()

                message = f'Пользователь {request.user.username} вышел из системы.'
                LogoutEvent()(request=self.request, user=request.user, msg=message)

                return Response({
                    'result': True,
                })

        return Response({
            'result': False,
        }, status=401)


logout_view = LogoutView.as_view()
