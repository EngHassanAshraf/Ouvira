from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user_with_role(self, **extra_fields):
        from .models import CustomUser

        if self.model.objects.count() == 0:
            extra_fields["user_role"] = "account_owner"
        else:
            extra_fields.setdefault("user_role", "employee")


        user = self.model(**extra_fields)
        user.set_password(extra_fields.get("password"))
        user.save(using=self._db)
        return user
