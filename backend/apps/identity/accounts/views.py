import datetime
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from apps.identity.auth_module.serializers import  RegisterOwnerSerializer
from apps.identity.shared.exceptions import BusinessException
from .services import UserService, RoleService
from apps.identity.shared.messages.error import ERROR_MESSAGES
from apps.identity.shared.messages.success import SUCCESS_MESSAGES
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle




class RegisterOwnerView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "register_owner"

    swagger_auto_schema(request_body=RegisterOwnerSerializer)
    def post(self, request):
        serializer = RegisterOwnerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = UserService.update_existing_user(**serializer.validated_data)

        except BusinessException as e:
            return Response(
                {"status":"error",
                 "message": e.message},
                status=status.HTTP_400_BAD_REQUEST
            )
        except ValueError as e:
            return Response(
                {"status": "error", 'message':str(e)},
                      status=status.HTTP_400_BAD_REQUEST
            )

        except PermissionError as e:
            return Response(
                {"status": "error", "message": str(e)},
                status=status.HTTP_403_FORBIDDEN
            )

        except Exception as e:
            return Response(
                {"status": "error", "message": ERROR_MESSAGES["SYSTEM_ERROR"]},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            {"status":"success", "message": SUCCESS_MESSAGES["ASSIGNED_AS_OWNER"]},
            status=status.HTTP_200_OK
        )


class ChangeUserRoleView(APIView):
    permission_classes = [IsAuthenticated]


    def post(self, request, user_id):
        new_role = request.data.get("new_role")

        if not new_role:
            return Response({"error": "new_role mandatory"}, status=400)

        try:
            user = RoleService.change_user_role(
                request.user,
                user_id,
                new_role
            )
        except PermissionDenied as e:
            return Response({"error": str(e)}, status=403)
        except ValueError as e:
            return Response({"error": str(e)}, status=400)

        return Response(
            {"msg": f"{user.username}, Role {user.user_role}, ga o'zgartirildi"}, status=200
        )


class SessionTestAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user = request.user
        token = request.auth

        if hasattr(token, 'payload'):
            exp_timestamp = token.payload.get('exp')  # integer
        else:
            exp_timestamp = None

        if exp_timestamp:
            exp_datetime = datetime.datetime.fromtimestamp(exp_timestamp)
        else:
            exp_datetime = None

        return Response({
            "user": str(user),
            "token_expires_at": exp_datetime,
        })
