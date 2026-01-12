from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import CustomUser
from auth_module.models import OTP
from core.messages.error import ERROR_MESSAGES
from core.messages.success import SUCCESS_MESSAGES

class SignUPViewTests(APITestCase):

    def setUp(self):
        self.url = reverse("signup")
        self.phone = "+998901234567"  # ✅ regex validator mos format
        self.full_name = "Husniddin Mirzayev"

    def post(self, phone=None, name=None):
        data = {
            "primary_mobile": phone if phone is not None else self.phone,
            "full_name": name if name is not None else self.full_name
        }
        return self.client.post(self.url, data, format="json")

    def test_signup_scenarios(self):
        scenarios = [
            {
                "name": "missing_fields",
                "phone": "",
                "name": "",
                "expected_status": status.HTTP_400_BAD_REQUEST,
                "expected_message": None
            },
            {
                "name": "new_user_success",
                "phone": self.phone,
                "name": self.full_name,
                "expected_status": status.HTTP_200_OK,
                "expected_message": SUCCESS_MESSAGES["PHONE_OTP_SENT"]
            },
            {
                "name": "duplicate_user",
                "phone": self.phone,
                "name": self.full_name,
                "setup": lambda: CustomUser.objects.create(
                    primary_mobile=self.phone,
                    full_name=self.full_name,
                    username=self.full_name
                ),
                "expected_status": status.HTTP_200_OK,
                "expected_message": SUCCESS_MESSAGES["PHONE_OTP_SENT"]
            },
        ]

        for scenario in scenarios:
            with self.subTest(scenario=scenario["name"]):
                # DB ni tozalash
                CustomUser.objects.all().delete()
                OTP.objects.all().delete()

                # duplicate user setup
                if "setup" in scenario:
                    scenario["setup"]()

                response = self.post(scenario["phone"], scenario.get("name"))

                # Status code tekshirish
                self.assertEqual(response.status_code, scenario["expected_status"])

                if response.status_code == status.HTTP_200_OK:
                    self.assertIn("message", response.data)
                    self.assertEqual(response.data["message"], scenario["expected_message"])

                    otp = OTP.objects.filter(phone_number=scenario["phone"] or self.phone).first()
                    self.assertIsNotNone(otp)
                    self.assertEqual(len(otp.otp_code), 6)

                else:
                    # serializer 400 response uchun kalitlar tekshir
                    self.assertTrue("primary_mobile" in response.data or "full_name" in response.data)