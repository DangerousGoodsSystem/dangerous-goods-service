from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import Customer

User = get_user_model()

@receiver(pre_save, sender=Customer)
def sync_user_email_on_customer_update(sender, instance, **kwargs):

    if not instance.pk:
        return

    try:
        old_customer = Customer.objects.get(pk=instance.pk)
    except Customer.DoesNotExist:
        return

    if old_customer.email == instance.email:
        return
        
    new_email = instance.email
    old_email = old_customer.email

    try:
        user_to_update = User.objects.get(email=old_email)

        if User.objects.filter(email=new_email).exclude(pk=user_to_update.pk).exists():
            raise ValidationError(
                {'email': f"Email '{new_email}' already in use by another account."}
            )
        
        user_to_update.email = new_email
        user_to_update.save(update_fields=['email'])

    except User.DoesNotExist:
        if User.objects.filter(email=new_email).exists():
            raise ValidationError(
                {'email': f"Email '{new_email}' already in use by another account."}
            )
