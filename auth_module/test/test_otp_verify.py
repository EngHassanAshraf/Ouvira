from datetime import timedelta
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import CustomUser
from auth_module.models import OTP
from core.messages.error import  ERROR_MESSAGES
from core.messages.success import SUCCESS_MESSAGES



class OTPVerifyViewTests(APITestCase):
    """
    Parametrized tests for OTP verification scenarios.
    Covers all critical edge cases defined in security review.
    """

    def setUp(self):
        self.url = reverse("verify-otp")
        self.phone = "998901234567"
        self.correct_code = "123456"

        self.user = CustomUser.objects.create(
            primary_mobile=self.phone,
            phone_verified=False
        )

    def create_otp(
        self,
        code=None,
        expires_at=None,
        attempts=0,
        is_blocked=False,
        blocked_until=None
    ):
        return OTP.objects.create(
            phone_number=self.phone,
            otp_code=code or self.correct_code,
            expires_at=expires_at or timezone.now() + timedelta(minutes=5),
            attempts=attempts,
            is_blocked=is_blocked,
            blocked_until=blocked_until
        )

    def post(self, code):
        return self.client.post(
            self.url,
            {
                "primary_mobile": self.phone,
                "otp_code": code
            },
            format="json"
        )

    def test_otp_verification_scenarios(self):
        """
        Parametrized OTP verification scenarios.
        """

        scenarios = [
            {
                "name": "expired_otp",
                "setup": lambda: self.create_otp(
                    expires_at=timezone.now() - timedelta(minutes=1)
                ),
                "code": self.correct_code,
                "expected_status": status.HTTP_400_BAD_REQUEST,
                "expected_message": ERROR_MESSAGES["OTP_EXPIRED"],
            },
            {
                "name": "incorrect_otp",
                "setup": lambda: self.create_otp(code="000000"),
                "code": "111111",
                "expected_status": status.HTTP_400_BAD_REQUEST,
                "expected_message": ERROR_MESSAGES["INCORRECT_OTP"],
            },
            {
                "name": "blocked_otp",
                "setup": lambda: self.create_otp(
                    is_blocked=True,
                    blocked_until=timezone.now() + timedelta(minutes=10)
                ),
                "code": self.correct_code,
                "expected_status": status.HTTP_403_FORBIDDEN,
                "expected_message": ERROR_MESSAGES["OTP_EXPIRED"],
            },
            {
                "name": "valid_otp",
                "setup": lambda: self.create_otp(),
                "code": self.correct_code,
                "expected_status": status.HTTP_200_OK,
                "expected_message": SUCCESS_MESSAGES["MOBILE_VALIDATED"],
            },
        ]

        for scenario in scenarios:
            with self.subTest(scenario=scenario["name"]):
                OTP.objects.all().delete()

                scenario["setup"]()
                response = self.post(scenario["code"])

                self.assertEqual(response.status_code, scenario["expected_status"])
                self.assertEqual(response.data["message"], scenario["expected_message"])

                if scenario["name"] == "valid_otp":
                    self.user.refresh_from_db()
                    self.assertTrue(self.user.phone_verified)
