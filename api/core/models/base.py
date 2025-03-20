from django.db import models
from django.utils.translation import gettext_lazy as _
from .managers import BaseModelManager


class BaseModel(models.Model):
    """
    Represents the base model containing all the commonly used fields

    Attributes:
    - created_at : (datetime)
        - The date and time when the record was created
    - updated_at : (datetime)
        - The date and time when the record got updated
    - is_deleted : (boolean)
        - Represents if a record is soft deleted
    """

    created_at = models.DateTimeField(
        _('Created date time'),
        auto_now_add=True,
        help_text=_('The date and time when the object was created')
    )
    updated_at = models.DateTimeField(
        _('Updated date time'),
        auto_now_add=True,
        help_text=_('The date and time when the object was updated')
    )
    is_deleted = models.BooleanField(
        _('is record deleted'),
        default=False,
        help_text=_('Represents if a record is soft deleted')
    )

    objects = BaseModelManager()

    class Meta:
        abstract = True
        ordering = ['updated_at']
