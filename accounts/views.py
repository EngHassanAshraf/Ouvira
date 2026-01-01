from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from auth_module.serializers import  RegisterOwnerSerializer
from core.exceptions import BusinessException
from .services import UserService, RoleService
from core.messages.error import ERROR_MESSAGES
from core.messages.success import SUCCESS_MESSAGES


class RegisterOwnerView(APIView):
    permission_classes = [AllowAny]
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
        except Exception:
            return Response(
                {
                    "status": "error",
                    'message':ERROR_MESSAGES["SYSTEM_ERROR"]},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            {"status":"success",
             "message": SUCCESS_MESSAGES["ASSIGNED_AS_OWNER"]},
            status=status.HTTP_200_OK
        )


class ChangeUserRoleView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request, user_id):
        new_role = request.data.get("new_role")
        user = RoleService.change_user_role(request.user, user_id, new_role)
        return  Response({"msg": f"{user.username} role {user.user_role} ga o'zgartirildi"})


class SessionTestAPIView(APIView):
    def get(self, request):
        remaining = request.session.get_expiry_age()  # session qolgan vaqti soniyada
        print(remaining, "vaqt")
        return Response(
            {"session_remaining_seconds": remaining},
            status=status.HTTP_200_OK
        )
