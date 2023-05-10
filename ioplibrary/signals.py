from django.apps import AppConfig
from django.core.signals import setting_changed
from django.db.models.signals import post_init, post_save, post_delete
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Book


@receiver(post_save, sender=Book)
def update_book_on_change(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "update_book", {"type": "book_change", "instance": instance.book_id}
    )


@receiver(post_delete, sender=Book)
def update_book_on_delete(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "update_book", {"type": "book_delete", "instance": instance.book_id}
    )
