from django.shortcuts import render
from django.db.models import Q
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.response import Response
from .permissions import IsStaffUser, IsUser, DjangoModelPermissionsWithView
from .pagination import CustomPagination

from .models import (
    UNCode,
    Classification,
    Division,
    CompatibilityGroup,
    PackingGroup,
    SpecialProvisions,
    ExceptedQuantities,
    PackingInstructions,
    PackingProvisions,
    IBCInstructions,
    IBCProvisions,
    TankInstructions,
    TankProvisions,
    EmergencySchedule,
    StowageHandling,
    Segregation,
    SegregationBar,
    DangerousGoods,
)
from .serializers import(
    UNCodeSerializer,
    ClassificationSerializer,
    DivisionSerializer,
    CompatibilityGroupSerializer,
    PackingGroupSerializer,
    SpecialProvisionsSerializer,
    ExceptedQuantitiesSerializer,
    PackingInstructionsSerializer,
    PackingProvisionsSerializer,
    IBCInstructionsSerializer,
    IBCProvisionsSerializer,
    TankInstructionsSerializer,
    TankProvisionsSerializer,
    EmergencyScheduleSerializer,
    StowageHandlingSerializer,
    SegregationSerializer,
    SegregationBarSerializer,
    DangerousGoodsSerializer,
)

class UNCodeViewSet(viewsets.ViewSet):
    permission_classes = [IsStaffUser, DjangoModelPermissionsWithView]
    pagination_class = CustomPagination
    queryset = UNCode.objects.filter(activate=True)
    
    def list(self, request):
        """List all UN Codes"""
        un_codes = self.queryset
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(un_codes, request)
        serializer = UNCodeSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        """Retrieve a UN Code by its primary key"""
        instance = get_object_or_404(self.queryset, pk=pk)
        serializer = UNCodeSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    @action(detail=False, methods=['get'], url_path='get-by-code', permission_classes=[IsUser])
    def get_by_code(self, request):
        """Retrieve a UN Code by its code"""
        code_param = request.query_params.get('code', None)
        if not code_param:
            return Response({"detail": "Missing 'code' parameter."}, status=status.HTTP_400_BAD_REQUEST)
        instance = get_object_or_404(self.queryset, code=code_param)
        serializer = UNCodeSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def create(self, request):
        """Create a new UN Code"""
        data = request.data
        many = isinstance(data, list)
        serializer = UNCodeSerializer(data=data, many=many)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def partial_update(self, request, pk=None):
        """Partially update a UN Code"""
        instance = get_object_or_404(self.queryset, pk=pk)
        serializer = UNCodeSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    def destroy(self, request, pk=None):
        """Delete a UN Code"""
        instance = get_object_or_404(self.queryset, pk=pk)
        instance.activate = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class ClassificationViewSet(viewsets.ViewSet):
    permission_classes = [IsStaffUser, DjangoModelPermissionsWithView]
    pagination_class = CustomPagination
    queryset = Classification.objects.filter(activate=True)

    def list(self, request):
        """
        List all Classifications
        """
        classifications = self.queryset
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(classifications, request)
        serializer = ClassificationSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    def retrieve(self, request, pk=None):
        """
        Retrieve a Classification by its primary key
        """
        instance = get_object_or_404(self.queryset, pk=pk)
        serializer = ClassificationSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def create(self, request):
        """
        Create a new Classification
        """
        data = request.data
        many = isinstance(data, list)
        serializer = ClassificationSerializer(data=data, many=many)
        serializer.is_valid(raise_exception=True)
        serializer.save() # single → ClassificationSerializer.create(); bulk → ListSerializer.create()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def partial_update(self, request, pk=None):
        """
        Partially update a Classification
        """
        instance = get_object_or_404(self.queryset, pk=pk)
        serializer = ClassificationSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    def destroy(self, request, pk=None):
        """
        Delete a Classification
        """
        instance = get_object_or_404(self.queryset, pk=pk)
        instance.activate = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class DivisionViewSet(viewsets.ViewSet):
    permission_classes = [IsStaffUser, DjangoModelPermissionsWithView]
    pagination_class = CustomPagination
    queryset = Division.objects.filter(activate=True)

    def list(self, request):
        """
        List all Divisions
        """
        divisions = self.queryset
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(divisions, request)
        serializer = DivisionSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    def retrieve(self, request, pk=None):
        """
        Retrieve a Division by its primary key
        """
        instance = get_object_or_404(self.queryset, pk=pk)
        serializer = DivisionSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def create(self, request):
        """
        Create a new Division
        """
        data = request.data
        many = isinstance(data, list)
        serializer = DivisionSerializer(data=data, many=many)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def partial_update(self, request, pk=None):
        """
        Partially update a Division
        """
        instance = get_object_or_404(self.queryset, pk=pk)
        serializer = DivisionSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    def destroy(self, request, pk=None):
        """
        Delete a Division
        """
        instance = get_object_or_404(self.queryset, pk=pk)
        instance.activate = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
"""
Compatibility Group ViewSet
"""
class CompatibilityGroupViewSet(viewsets.ViewSet):
    permission_classes = [IsStaffUser, DjangoModelPermissionsWithView]
    pagination_class = CustomPagination
    queryset = CompatibilityGroup.objects.filter(activate=True)

    def list(self, request):
        """
        List all Compatibility Groups
        """
        compatibility_groups = self.queryset
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(compatibility_groups, request)
        serializer = CompatibilityGroupSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    def retrieve(self, request, pk=None):
        """
        Retrieve a Compatibility Group by its primary key
        """
        instance = get_object_or_404(self.queryset, pk=pk)
        serializer = CompatibilityGroupSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def create(self, request):
        """
        Create a new Compatibility Group
        """
        data = request.data
        many = isinstance(data, list)
        serializer = CompatibilityGroupSerializer(data=data, many=many)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def partial_update(self, request, pk=None):
        """
        Partially update a Compatibility Group
        """
        instance = get_object_or_404(self.queryset, pk=pk)
        serializer = CompatibilityGroupSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    def destroy(self, request, pk=None):
        """
        Delete a Compatibility Group
        """
        instance = get_object_or_404(self.queryset, pk=pk)
        instance.activate = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
"""
Packing Group ViewSet
"""
class PackingGroupViewSet(viewsets.ViewSet):
    permission_classes = [IsStaffUser, DjangoModelPermissionsWithView]
    pagination_class = CustomPagination
    queryset = PackingGroup.objects.filter(activate=True)

    def list(self, request):
        """
        List all Packing Groups
        """
        packing_groups = self.queryset
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(packing_groups, request)
        serializer = PackingGroupSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    def retrieve(self, request, pk=None):
        """
        Retrieve a Packing Group by its primary key
        """
        instance = get_object_or_404(self.queryset, pk=pk)
        serializer = PackingGroupSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    @action(detail=False, methods=['get'], url_path='get-by-code', permission_classes=[IsUser])
    def get_by_code(self, request):
        """
        Retrieve a Packing Group by its code
        """
        code_param = request.query_params.get('code', None)
        if not code_param:
            return Response({"detail": "Missing 'code' parameter."}, status=status.HTTP_400_BAD_REQUEST)
        instance = get_object_or_404(self.queryset, code=code_param)
        serializer = UNCodeSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def create(self, request):
        """
        Create a new Packing Group
        """
        data = request.data
        many = isinstance(data, list)
        serializer = PackingGroupSerializer(data=data, many=many)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def partial_update(self, request, pk=None):
        """
        Partially update a Packing Group
        """
        instance = get_object_or_404(self.queryset, pk=pk)
        serializer = PackingGroupSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    def destroy(self, request, pk=None):
        """
        Delete a Packing Group
        """
        instance = get_object_or_404(self.queryset, pk=pk)
        instance.activate = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

"""
Special Provisions ViewSet
"""
class SpecialProvisionsViewSet(viewsets.ViewSet):
    permission_classes = [IsStaffUser, DjangoModelPermissionsWithView]
    pagination_class = CustomPagination
    queryset = SpecialProvisions.objects.filter(activate=True)

    def list(self, request):
        """
        List all Special Provisions
        """
        special_provisions = self.queryset
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(special_provisions, request)
        serializer = SpecialProvisionsSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    def retrieve(self, request, pk=None):
        """
        Retrieve a Special Provision by its primary key
        """
        instance = get_object_or_404(self.queryset, pk=pk)
        serializer = SpecialProvisionsSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    @action(detail=False, methods=['get'], url_path='get-by-code', permission_classes=[IsUser])
    def get_by_code(self, request):
        """
        Retrieve a Special Provision by its code
        """
        code_param = request.query_params.get('code', None)
        if not code_param:
            return Response({"detail": "Missing 'code' parameter."}, status=status.HTTP_400_BAD_REQUEST)
        instance = get_object_or_404(self.queryset, code=code_param)
        serializer = UNCodeSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def create(self, request):
        """
        Create a new Special Provision
        """
        data = request.data
        many = isinstance(data, list)
        serializer = SpecialProvisionsSerializer(data=data, many=many)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def partial_update(self, request, pk=None):
        """
        Partially update a Special Provision
        """
        instance = get_object_or_404(self.queryset, pk=pk)
        serializer = SpecialProvisionsSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    def destroy(self, request, pk=None):
        """
        Delete a Special Provision
        """
        instance = get_object_or_404(self.queryset, pk=pk)
        instance.activate = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

"""
Excepted Quantities ViewSet
"""
class ExceptedQuantitiesViewSet(viewsets.ViewSet):
    permission_classes = [IsStaffUser, DjangoModelPermissionsWithView]
    pagination_class = CustomPagination
    queryset = ExceptedQuantities.objects.filter(activate=True)

    def list(self, request):
        """
        List all Excepted Quantities
        """
        excepted_quantities = self.queryset
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(excepted_quantities, request)
        serializer = ExceptedQuantitiesSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    def retrieve(self, request, pk=None):
        """
        Retrieve an Excepted Quantity by its primary key
        """
        instance = get_object_or_404(self.queryset, pk=pk)
        serializer = ExceptedQuantitiesSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    @action(detail=False, methods=['get'], url_path='get-by-code', permission_classes=[IsUser])
    def get_by_code(self, request):
        """
        Retrieve an Excepted Quantity by its code
        """
        code_param = request.query_params.get('code', None)
        if not code_param:
            return Response({"detail": "Missing 'code' parameter."}, status=status.HTTP_400_BAD_REQUEST)
        instance = get_object_or_404(self.queryset, code=code_param)
        serializer = UNCodeSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def create(self, request):
        """
        Create a new Excepted Quantity
        """
        data = request.data
        many = isinstance(data, list)
        serializer = ExceptedQuantitiesSerializer(data=data, many=many)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def partial_update(self, request, pk=None):
        """
        Partially update an Excepted Quantity
        """
        instance = get_object_or_404(self.queryset, pk=pk)
        serializer = ExceptedQuantitiesSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    def destroy(self, request, pk=None):
        """
        Delete an Excepted Quantity
        """
        instance = get_object_or_404(self.queryset, pk=pk)
        instance.activate = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

"""
Packing Instructions ViewSet
"""
class PackingInstructionsViewSet(viewsets.ViewSet):
    permission_classes = [IsStaffUser, DjangoModelPermissionsWithView]
    pagination_class = CustomPagination
    queryset = PackingInstructions.objects.filter(activate=True)

    def list(self, request):
        """
        List all Packing Instructions
        """
        packing_instructions = self.queryset
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(packing_instructions, request)
        serializer = PackingInstructionsSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    def retrieve(self, request, pk=None):
        """
        Retrieve a Packing Instruction by its primary key
        """
        instance = get_object_or_404(self.queryset, pk=pk)
        serializer = PackingInstructionsSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    @action(detail=False, methods=['get'], url_path='get-by-code', permission_classes=[IsUser])
    def get_by_code(self, request):
        """
        Retrieve a Packing Instruction by its code
        """
        code_param = request.query_params.get('code', None)
        if not code_param:
            return Response({"detail": "Missing 'code' parameter."}, status=status.HTTP_400_BAD_REQUEST)
        instance = get_object_or_404(self.queryset, code=code_param)
        serializer = UNCodeSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def create(self, request):
        """
        Create a new Packing Instruction
        """
        data = request.data
        many = isinstance(data, list)
        serializer = PackingInstructionsSerializer(data=data, many=many)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def partial_update(self, request, pk=None):
        """
        Partially update a Packing Instruction
        """
        instance = get_object_or_404(self.queryset, pk=pk)
        serializer = PackingInstructionsSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    def destroy(self, request, pk=None):
        """
        Delete a Packing Instruction
        """
        instance = get_object_or_404(self.queryset, pk=pk)
        instance.activate = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

"""
Packing Provisions ViewSet
"""
class PackingProvisionsViewSet(viewsets.ViewSet):
    permission_classes = [IsStaffUser, DjangoModelPermissionsWithView]
    pagination_class = CustomPagination
    queryset = PackingProvisions.objects.filter(activate=True)

    def list(self, request):
        """
        List all Packing Provisions
        """
        packing_provisions = self.queryset
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(packing_provisions, request)
        serializer = PackingProvisionsSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    def retrieve(self, request, pk=None):
        """
        Retrieve a Packing Provision by its primary key
        """
        instance = get_object_or_404(self.queryset, pk=pk)
        serializer = PackingProvisionsSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    @action(detail=False, methods=['get'], url_path='get-by-code', permission_classes=[IsUser])
    def get_by_code(self, request):
        """
        Retrieve a Packing Provision by its code
        """
        code_param = request.query_params.get('code', None)
        if not code_param:
            return Response({"detail": "Missing 'code' parameter."}, status=status.HTTP_400_BAD_REQUEST)
        instance = get_object_or_404(self.queryset, code=code_param)
        serializer = UNCodeSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def create(self, request):
        """
        Create a new Packing Provision
        """
        data = request.data
        many = isinstance(data, list)
        serializer = PackingProvisionsSerializer(data=data, many=many)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def partial_update(self, request, pk=None):
        """
        Partially update a Packing Provision
        """
        instance = get_object_or_404(self.queryset, pk=pk)
        serializer = PackingProvisionsSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    def destroy(self, request, pk=None):
        """
        Delete a Packing Provision
        """
        instance = get_object_or_404(self.queryset, pk=pk)
        instance.activate = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

"""
IBC Instructions ViewSet
"""
class IBCInstructionsViewSet(viewsets.ViewSet):
    permission_classes = [IsStaffUser, DjangoModelPermissionsWithView]
    pagination_class = CustomPagination
    queryset = IBCInstructions.objects.filter(activate=True)

    def list(self, request):
        """
        List all IBC Instructions
        """
        ibc_instructions = self.queryset
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(ibc_instructions, request)
        serializer = IBCInstructionsSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    def retrieve(self, request, pk=None):
        """
        Retrieve an IBC Instruction by its primary key
        """
        instance = get_object_or_404(self.queryset, pk=pk)
        serializer = IBCInstructionsSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    @action(detail=False, methods=['get'], url_path='get-by-code', permission_classes=[IsUser])
    def get_by_code(self, request):
        """
        Retrieve an IBC Instruction by its code
        """
        code_param = request.query_params.get('code', None)
        if not code_param:
            return Response({"detail": "Missing 'code' parameter."}, status=status.HTTP_400_BAD_REQUEST)
        instance = get_object_or_404(self.queryset, code=code_param)
        serializer = UNCodeSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def create(self, request):
        """
        Create a new IBC Instruction
        """
        data = request.data
        many = isinstance(data, list)
        serializer = IBCInstructionsSerializer(data=data, many=many)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def partial_update(self, request, pk=None):
        """
        Partially update an IBC Instruction
        """
        instance = get_object_or_404(self.queryset, pk=pk)
        serializer = IBCInstructionsSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    def destroy(self, request, pk=None):
        """
        Delete an IBC Instruction
        """
        instance = get_object_or_404(self.queryset, pk=pk)
        instance.activate = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

"""
IBC Provisions ViewSet
"""
class IBCProvisionsViewSet(viewsets.ViewSet):
    permission_classes = [IsStaffUser, DjangoModelPermissionsWithView]
    pagination_class = CustomPagination
    queryset = IBCProvisions.objects.filter(activate=True)

    def list(self, request):
        """
        List all IBC Provisions
        """
        ibc_provisions = self.queryset
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(ibc_provisions, request)
        serializer = IBCProvisionsSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    @action(detail=False, methods=['get'], url_path='get-by-code', permission_classes=[IsUser])
    def get_by_code(self, request):
        """
        Retrieve an IBC Provision by its code
        """
        code_param = request.query_params.get('code', None)
        if not code_param:
            return Response({"detail": "Missing 'code' parameter."}, status=status.HTTP_400_BAD_REQUEST)
        instance = get_object_or_404(self.queryset, code=code_param)
        serializer = UNCodeSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def retrieve(self, request, pk=None):
        """
        Retrieve an IBC Provision by its primary key
        """
        instance = get_object_or_404(self.queryset, pk=pk)
        serializer = IBCProvisionsSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        """
        Create a new IBC Provision
        """
        data = request.data
        many = isinstance(data, list)
        serializer = IBCProvisionsSerializer(data=data, many=many)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def partial_update(self, request, pk=None):
        """
        Partially update an IBC Provision
        """
        instance = get_object_or_404(self.queryset, pk=pk)
        serializer = IBCProvisionsSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    def destroy(self, request, pk=None):
        """
        Delete an IBC Provision
        """
        instance = get_object_or_404(self.queryset, pk=pk)
        instance.activate = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

"""
Tank Instructions ViewSet
"""
class TankInstructionsViewSet(viewsets.ViewSet):
    permission_classes = [IsStaffUser, DjangoModelPermissionsWithView]
    pagination_class = CustomPagination
    queryset = TankInstructions.objects.filter(activate=True)

    def list(self, request):
        """
        List all Tank Instructions
        """
        tank_instructions = self.queryset
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(tank_instructions, request)
        serializer = TankInstructionsSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    def retrieve(self, request, pk=None):
        """
        Retrieve a Tank Instruction by its primary key
        """
        instance = get_object_or_404(self.queryset, pk=pk)
        serializer = TankInstructionsSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    @action(detail=False, methods=['get'], url_path='get-by-code', permission_classes=[IsUser])
    def get_by_code(self, request):
        """
        Retrieve a Tank Instruction by its code
        """
        code_param = request.query_params.get('code', None)
        if not code_param:
            return Response({"detail": "Missing 'code' parameter."}, status=status.HTTP_400_BAD_REQUEST)
        instance = get_object_or_404(self.queryset, code=code_param)
        serializer = UNCodeSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def create(self, request):
        """
        Create a new Tank Instruction
        """
        data = request.data
        many = isinstance(data, list)
        serializer = TankInstructionsSerializer(data=data, many=many)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def partial_update(self, request, pk=None):
        """
        Partially update a Tank Instruction
        """
        instance = get_object_or_404(self.queryset, pk=pk)
        serializer = TankInstructionsSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    def destroy(self, request, pk=None):
        """
        Delete a Tank Instruction
        """
        instance = get_object_or_404(self.queryset, pk=pk)
        instance.activate = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


"""
Tank Provisions ViewSet
"""
class TankProvisionsViewSet(viewsets.ViewSet):
    permission_classes = [IsStaffUser, DjangoModelPermissionsWithView]
    pagination_class = CustomPagination
    queryset = TankProvisions.objects.filter(activate=True)

    def list(self, request):
        """
        List all Tank Provisions
        """
        tank_provisions = self.queryset
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(tank_provisions, request)
        serializer = TankProvisionsSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    def retrieve(self, request, pk=None):
        """
        Retrieve a Tank Provision by its primary key
        """
        instance = get_object_or_404(self.queryset, pk=pk)
        serializer = TankProvisionsSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    @action(detail=False, methods=['get'], url_path='get-by-code', permission_classes=[IsUser])
    def get_by_code(self, request):
        """
        Retrieve a Tank Provision by its code
        """
        code_param = request.query_params.get('code', None)
        if not code_param:
            return Response({"detail": "Missing 'code' parameter."}, status=status.HTTP_400_BAD_REQUEST)
        instance = get_object_or_404(self.queryset, code=code_param)
        serializer = UNCodeSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def create(self, request):
        """
        Create a new Tank Provision
        """
        data = request.data
        many = isinstance(data, list)
        serializer = TankProvisionsSerializer(data=data, many=many)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def partial_update(self, request, pk=None):
        """
        Partially update a Tank Provision
        """
        instance = get_object_or_404(self.queryset, pk=pk)
        serializer = TankProvisionsSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    def destroy(self, request, pk=None):
        """
        Delete a Tank Provision
        """
        instance = get_object_or_404(self.queryset, pk=pk)
        instance.activate = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

"""
Emergency Schedule ViewSet
"""
class EmergencyScheduleViewSet(viewsets.ViewSet):
    permission_classes = [IsStaffUser, DjangoModelPermissionsWithView]
    pagination_class = CustomPagination
    queryset = EmergencySchedule.objects.filter(activate=True)

    def list(self, request):
        """
        List all Emergency Schedules
        """
        emergency_schedules = self.queryset
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(emergency_schedules, request)
        serializer = EmergencyScheduleSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    def retrieve(self, request, pk=None):
        """
        Retrieve an Emergency Schedule by its primary key
        """
        instance = get_object_or_404(self.queryset, pk=pk)
        serializer = EmergencyScheduleSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    @action(detail=False, methods=['get'], url_path='get-by-code', permission_classes=[IsUser])
    def get_by_code(self, request):
        """
        Retrieve an Emergency Schedule by its code
        """
        code_param = request.query_params.get('code', None)
        if not code_param:
            return Response({"detail": "Missing 'code' parameter."}, status=status.HTTP_400_BAD_REQUEST)
        instance = get_object_or_404(self.queryset, code=code_param)
        serializer = UNCodeSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def create(self, request):
        """
        Create a new Emergency Schedule
        """
        data = request.data
        many = isinstance(data, list)
        serializer = EmergencyScheduleSerializer(data=data, many=many)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def partial_update(self, request, pk=None):
        """
        Partially update an Emergency Schedule
        """
        instance = get_object_or_404(self.queryset, pk=pk)
        serializer = EmergencyScheduleSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    def destroy(self, request, pk=None):
        """
        Delete an Emergency Schedule
        """
        instance = get_object_or_404(self.queryset, pk=pk)
        instance.activate = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

"""
Stowage Handling ViewSet
"""
class StowageHandlingViewSet(viewsets.ViewSet):
    permission_classes = [IsStaffUser, DjangoModelPermissionsWithView]
    pagination_class = CustomPagination
    queryset = StowageHandling.objects.filter(activate=True)

    def list(self, request):
        """
        List all Stowage Handlings
        """
        stowage_handlings = self.queryset
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(stowage_handlings, request)
        serializer = StowageHandlingSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    def retrieve(self, request, pk=None):
        """
        Retrieve a Stowage Handling by its primary key
        """
        instance = get_object_or_404(self.queryset, pk=pk)
        serializer = StowageHandlingSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    @action(detail=False, methods=['get'], url_path='get-by-code', permission_classes=[IsUser])
    def get_by_code(self, request):
        """
        Retrieve a Stowage Handling by its code
        """
        code_param = request.query_params.get('code', None)
        if not code_param:
            return Response({"detail": "Missing 'code' parameter."}, status=status.HTTP_400_BAD_REQUEST)
        instance = get_object_or_404(self.queryset, code=code_param)
        serializer = UNCodeSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def create(self, request):
        """
        Create a new Stowage Handling
        """
        data = request.data
        many = isinstance(data, list)
        serializer = StowageHandlingSerializer(data=data, many=many)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def partial_update(self, request, pk=None):
        """
        Partially update a Stowage Handling
        """
        instance = get_object_or_404(self.queryset, pk=pk)
        serializer = StowageHandlingSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    def destroy(self, request, pk=None):
        """
        Delete a Stowage Handling
        """
        instance = get_object_or_404(self.queryset, pk=pk)
        instance.activate = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

"""
Segregation ViewSet
"""
class SegregationViewSet(viewsets.ViewSet):
    permission_classes = [IsStaffUser, DjangoModelPermissionsWithView]
    pagination_class = CustomPagination
    queryset = Segregation.objects.filter(activate=True)

    def list(self, request):
        """
        List all Segregations
        """
        segregations = self.queryset
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(segregations, request)
        serializer = SegregationSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    def retrieve(self, request, pk=None):
        """
        Retrieve a Segregation by its primary key
        """
        instance = get_object_or_404(self.queryset, pk=pk)
        serializer = SegregationSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    @action(detail=False, methods=['get'], url_path='get-by-code', permission_classes=[IsUser])
    def get_by_code(self, request):
        """
        Retrieve a Segregation by its code
        """
        code_param = request.query_params.get('code', None)
        if not code_param:
            return Response({"detail": "Missing 'code' parameter."}, status=status.HTTP_400_BAD_REQUEST)
        instance = get_object_or_404(self.queryset, code=code_param)
        serializer = SegregationSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def create(self, request):
        """
        Create a new Segregation
        """
        data = request.data
        many = isinstance(data, list)
        serializer = SegregationSerializer(data=data, many=many)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def partial_update(self, request, pk=None):
        """
        Partially update a Segregation
        """
        instance = get_object_or_404(self.queryset, pk=pk)
        serializer = SegregationSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    def destroy(self, request, pk=None):
        """
        Delete a Segregation
        """
        instance = get_object_or_404(self.queryset, pk=pk)
        instance.activate = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

"""
Segregation Bar ViewSet
"""
class SegregationBarViewSet(viewsets.ViewSet):
    permission_classes = [IsStaffUser, DjangoModelPermissionsWithView]
    queryset = SegregationBar.objects.filter(activate=True)
    
    def list(self, request):
        """
        List all Segregation Bars
        """
        segregations = self.queryset
        serializer = SegregationBarSerializer(segregations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def retrieve(self, request, pk=None):
        """
        Retrieve a Segregation Bar by its primary key
        """
        instance = get_object_or_404(self.queryset, pk=pk)
        serializer = SegregationBarSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def create(self, request):
        """
        Create a new Segregation Bar
        """
        data = request.data
        many = isinstance(data, list)
        serializer = SegregationBarSerializer(data=data, many=many)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def partial_update(self, request, pk=None):
        """
        Partially update a Segregation Bar
        """
        instance = get_object_or_404(self.queryset, pk=pk)
        serializer = SegregationBarSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    def destroy(self, request, pk=None):
        """
        Delete a Segregation Bar
        """
        instance = get_object_or_404(self.queryset, pk=pk)
        instance.activate = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

"""
Dangerous Goods ViewSet
"""
class DangerousGoodsViewSet(viewsets.ViewSet):
    permission_classes = [IsStaffUser, DjangoModelPermissionsWithView]
    pagination_class = CustomPagination
    queryset = DangerousGoods.objects.all()

    def list(self, request):
        """
        List all Dangerous Goods
        """
        dangerous_goods = self.queryset
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(dangerous_goods, request)
        serializer = DangerousGoodsSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    def retrieve(self, request, pk=None):
        """
        Retrieve a Dangerous Good by its primary key
        """
        instance = get_object_or_404(self.queryset, pk=pk)
        serializer = DangerousGoodsSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def create(self, request):
        """
        Create a new Dangerous Good
        """
        data = request.data
        many = isinstance(data, list)
        serializer = DangerousGoodsSerializer(data=data, many=many)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def partial_update(self, request, pk=None):
        """
        Partially update a Dangerous Good
        """
        instance = get_object_or_404(self.queryset, pk=pk)
        serializer = DangerousGoodsSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    def destroy(self, request, pk=None):
        """
        Delete a Dangerous Good
        """
        instance = get_object_or_404(self.queryset, pk=pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class SearchDangerousGoodsViewSet(viewsets.ViewSet):
    permission_classes = [IsUser]
    pagination_class = CustomPagination
    queryset = DangerousGoods.objects.all()

    def list(self, request):
        """
        Search Dangerous Goods
        """
        search_term = request.query_params.get('search', None)
        if not search_term:
            return Response({"detail": "Missing 'search' parameter."}, status=status.HTTP_400_BAD_REQUEST)

        dangerous_goods = self.queryset.filter(
            Q(uncode__code=search_term, uncode__activate=True)
        )

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(dangerous_goods, request)
        serializer = DangerousGoodsSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    def retrieve(self, request, pk=None):
        """
        Retrieve a Dangerous Good by its primary key
        """
        instance = get_object_or_404(self.queryset, pk=pk)
        serializer = DangerousGoodsSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)