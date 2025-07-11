from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from .pagination import CustomPagination
from .permissions import IsStaffUser, DjangoModelPermissionsWithView
from .models import Customer
from .serializers import CustomerSerializer

class CustomerViewSet(viewsets.ViewSet):
    permission_classes = [IsStaffUser, DjangoModelPermissionsWithView]
    pagination_class = CustomPagination

    def get_queryset(self):
        return Customer.objects.all()
    
    def list(self, request):
        customers = self.get_queryset()
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(customers, request)
        serializer = CustomerSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        customer = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def create(self, request):
        is_many = isinstance(request.data, list)
        list_data = request.data if is_many else [request.data]
        serializer = CustomerSerializer(data=list_data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_data = serializer.data if is_many else serializer.data[0]
        return Response(response_data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, pk=None):
        customer = get_object_or_404(self.get_queryset(), pk=pk)
        serializer = CustomerSerializer(customer, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        customer = get_object_or_404(self.get_queryset(), pk=pk)
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)