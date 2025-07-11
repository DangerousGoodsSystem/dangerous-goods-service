from rest_framework import serializers
from .models import Customer
from .tasks import create_users_for_new_customers

class CustomerListCreateSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        incoming_emails = [item['email'] for item in validated_data]
        
        if len(incoming_emails) != len(set(incoming_emails)):
            raise serializers.ValidationError('Uploaded data has duplicate email.')

        existing_customers = Customer.objects.filter(email__in=incoming_emails)
        existing_emails = set(existing_customers.values_list('email', flat=True))

        if existing_emails:
            raise serializers.ValidationError(f"The following emails already exist: {', '.join(existing_emails)}")
        
        customers_to_create = [Customer(**item) for item in validated_data]
        created_customers = Customer.objects.bulk_create(customers_to_create)

        customer_data_for_task = [
            {'email': item['email'], 'name': item.get('name', '')} for item in validated_data
        ]

        create_users_for_new_customers.delay(customer_data_for_task)

        return created_customers

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'date_joined']
        list_serializer_class = CustomerListCreateSerializer