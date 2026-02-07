from django.db import models
from django.utils.translation import gettext_lazy as _


class Company(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", _("Active")
        DEACTIVATED = "deactivated", _("Deactivated")
        DELETED = "deleted", _("Deleted")

    name = models.CharField(max_length=255, verbose_name=("Company name"))
    logo = models.ImageField(upload_to="companies/logo", null=True, blank=True, verbose_name=_("Company logo"))
    address = models.TextField(null=True, blank=True, verbose_name=_("Company address"))
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE, verbose_name=_("Status"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        db_table = "companies"
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

