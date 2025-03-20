from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from api.core.models import BaseModelManager


@receiver(pre_save)
def update_timestamp(sender, instance, *args, **kwargs):
    instance.updated_at = timezone.now()


pre_save.connect(update_timestamp, sender=BaseModelManager)
