from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from planetarium.models import Ticket


@receiver([post_delete, post_save], sender=Ticket)
def invalidate_ticket_cache(sender, instance, **kwargs):
    cache.delete("ticket_view:*")
