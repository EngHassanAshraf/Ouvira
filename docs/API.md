# POST /api/signup/ #
Foydalanuvchi yangi account yaratadi va telefon raqamiga OTP yuboriladi.
Telefon raqami va full name bilan yangi user yaratish yoki mavjud userni olish
Yangi OTP generatsiya qilinadi va 5 daqiqa davomida amal qiladi


Request Body 
json
    {
      "primary_mobile": "string",   // required, foydalanuvchi telefon raqami
      "full_name": "string"         // required, foydalanuvchi to‘liq ismi
    }
Response Examples
Success (200 OK) : 
json:
    {
      "status": "success",
      "message": "Verification code sent to your mobile number.",
      "expiry": "5 minutes"
    }
Warning (400 Bad Request) :
json:
    {
      "status": "warning",
      "message": "Missing required fields."
    }

Error (500 Internal Server Error)
json:
    {
      "status": "error",
      "message": "An unexpected error occurred. Please try again later."
    }

Har safar SignUp chaqirilganda eski OTP’lar o‘chiriladi
OTP muddati: 5 daqiqa
Response format:

json:
    {
      "status": "success | warning | error",
      "message": "string",
      "expiry": "string (success holatda)"
    }

# POST /api/otp-verify/ #

Foydalanuvchi telefon raqamini verify qilish uchun yuborilgan OTP kodini tekshiradi.
Telefon raqami va OTP to‘g‘ri bo‘lsa, foydalanuvchi phone_verified = True bo‘ladi
Agar OTP noto‘g‘ri, muddati o‘tgan yoki attempts ko‘p bo‘lsa, mos xabar qaytariladi


AllowAny (login qilmagan foydalanuvchi ham ishlata oladi)
Request Body
_{
  "primary_mobile": "string",   // required, foydalanuvchi telefon raqami
  "otp_code": "string"          // required, foydalanuvchiga yuborilgan 6 raqamli kod
}_

Response Examples
Success (200 OK)
{
  "status": "success",
  "message": "Mobile number verified successfully"
}

Warning (400 Bad Request)
{
  "status": "warning",
  "message": "Missing required fields."
}


Error (400 / 403)
OTP expired
{
  "status": "error",
  "message": "The verification code has expired. Please request a new one."
}


Incorrect OTP
{
  "status": "error",
  "message": "The verification code is incorrect. You have 2 attempts left."
}


Too many attempts (blocked)
{
  "status": "error",
  "message": "Too many failed attempts. Try again later."
}


User not found
{
  "status": "error",
  "message": "No account was found with the provided information."
}

OTP muddati: 5 daqiqa
Maksimal urinishlar: 5
Block vaqt: 10 daqiqa

Response format:
{
  "status": "success | warning | error",
  "message": "string"
}