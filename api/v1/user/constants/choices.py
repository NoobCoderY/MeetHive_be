
from django.db import models
from django.utils.translation import gettext_lazy as _


class AuditLogTaskChoices(models.TextChoices):
    CREATE_TRANSCRIPTION = "CREATE_TRANSCRIPTION", _("Create Transcription")
    UPDATE_TRANSCRIPTION = "UPDATE_TRANSCRIPTION", _("Update Transcription")
    DELETE_TRANSCRIPTION = "DELETE_TRANSCRIPTION", _("Delete Transcription")
    CREATE_SUMMARY      =   "CREATE_SUMMARY", _("Create Summary")
    UPDATE_SUMMARY      =   "UPDATE_SUMMARY ", _("Update  Summary")
    DELETE_SUMMARY      =   "DELETE_SUMMARY ", _("Delete  Summary")
