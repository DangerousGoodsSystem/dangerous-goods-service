from django.conf import settings
from celery import shared_task
from django.contrib.auth import get_user_model

User = get_user_model()

@shared_task
def create_users_for_new_customers(customer_data_list):
    
    emails_to_check = [item['email'] for item in customer_data_list]
    existing_user_emails = set(User.objects.filter(email__in=emails_to_check).values_list('email', flat=True))

    users_to_create = []
    for customer_data in customer_data_list:
        email = customer_data.get('email')
        
        if not email or email in existing_user_emails:
            continue

        name = customer_data.get('name', '')
        name_parts = name.strip().split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''

        user = User(
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(settings.DEFAULT_CUSTOMER_PASSWORD)

        users_to_create.append(user)

    if users_to_create:
        try:
            User.objects.bulk_create(users_to_create)
        except Exception as e:
            print(f"Error when execute bulk_create: {e}")

    return f"Processed and created successfully {len(users_to_create)}/{len(customer_data_list)} user."
