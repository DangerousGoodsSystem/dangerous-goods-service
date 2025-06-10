from django.db import IntegrityError
from rest_framework import serializers
from .services import IMDGLookupService
from .models import (
    IMDGAmendment,
    UNCode,
    ClassDivision,
    PackingGroup,
    SpecialProvisions,
    ExceptedQuantities,
    PackingInstructions,
    PackingProvisions,
    IBCInstructions,
    IBCProvisions,
    TankInstructions,
    TankProvisions,
    EmergencySchedules,
    StowageHandling,
    Segregation,
    SegregationRule,
    DangerousGoods,
)

class IMDGAmendmentSerializer(serializers.ModelSerializer):
    """Serializer for IMDGAmendment model."""
    class Meta:
        model = IMDGAmendment
        fields = ['id',
                  'name',
                  'is_effective',
                  'upload_at']

class BaseListSerializer(serializers.ListSerializer):
    """
    Custom ListSerializer to handle bulk creation with detailed error reporting.
    """
    def create(self, validated_data):
        lookup_service = IMDGLookupService()
        if not lookup_service.active_amendment:
            raise serializers.ValidationError("No active amendment found.")
        
        instances = []
        errors = []
        for idx, item_data in enumerate(validated_data):
            item_data['imdgamendment'] = lookup_service.active_amendment
            try:
                inst = self.child.create(item_data)
                instances.append(inst)
                errors.append(None)
            except serializers.ValidationError as exc:
                errors.append(exc.detail)
                instances.append(None)

        if not any(errors):
            return instances

        raise serializers.ValidationError({
            'results': instances,
            'errors': errors
        })

class UNCodeSerializer(serializers.ModelSerializer):
    """Custom serializer for UNCode model with bulk creation support."""
    class Meta:
        model = UNCode
        fields = ['id',
                  'code',
                  'description']
        list_serializer_class = BaseListSerializer
    
    def create(self, validated_data):
        lookup_service = IMDGLookupService()
        if not lookup_service.active_amendment:
            raise serializers.ValidationError("No active amendment found.")
        validated_data['imdgamendment'] = lookup_service.active_amendment
        
        try:
            return super().create(validated_data)
        except IntegrityError as e:
            raise serializers.ValidationError({
                'code': ['This code already exists in the current amendment.']
            }) from e


class ClassDivisionSerializer(serializers.ModelSerializer):
    """Custom serializer for Classification model with bulk creation support."""
    class Meta:
        model = ClassDivision
        fields = ['id',
                  'code',
                  'label',
                  'description']
        list_serializer_class = BaseListSerializer

    def create(self, validated_data):
        lookup_service = IMDGLookupService()
        if not lookup_service.active_amendment:
            raise serializers.ValidationError("No active amendment found.")
        validated_data['imdgamendment'] = lookup_service.active_amendment
        
        try:
            return super().create(validated_data)
        except IntegrityError as e:
            raise serializers.ValidationError({
                'code': ['This code already exists in the current amendment.']
            }) from e


class PackingGroupSerializer(serializers.ModelSerializer):
    """Custom serializer for PackingGroup model with bulk creation support."""
    class Meta:
        model = PackingGroup
        fields = ['id',
                  'code',
                  'file',
                  'description',
                  ]
        list_serializer_class = BaseListSerializer

    def create(self, validated_data):
        lookup_service = IMDGLookupService()
        if not lookup_service.active_amendment:
            raise serializers.ValidationError("No active amendment found.")
        validated_data['imdgamendment'] = lookup_service.active_amendment
        
        try:
            return super().create(validated_data)
        except IntegrityError as e:
            raise serializers.ValidationError({
                'code': ['This code already exists in the current amendment.']
            }) from e


class SpecialProvisionsSerializer(serializers.ModelSerializer):
    """Custom serializer for SpecialProvisions model with bulk creation support."""
    class Meta:
        model = SpecialProvisions
        fields = ['id',
                  'code',
                  'file',
                  'description']
        list_serializer_class = BaseListSerializer

    def create(self, validated_data):
        lookup_service = IMDGLookupService()
        if not lookup_service.active_amendment:
            raise serializers.ValidationError("No active amendment found.")
        validated_data['imdgamendment'] = lookup_service.active_amendment
        
        try:
            return super().create(validated_data)
        except IntegrityError as e:
            raise serializers.ValidationError({
                'code': ['This code already exists in the current amendment.']
            }) from e


class ExceptedQuantitiesSerializer(serializers.ModelSerializer):
    """Custom serializer for ExceptedQuantities model with bulk creation support."""
    class Meta:
        model = ExceptedQuantities
        fields = ['id',
                  'code',
                  'file',
                  'description']
        list_serializer_class = BaseListSerializer

    def create(self, validated_data):
        lookup_service = IMDGLookupService()
        if not lookup_service.active_amendment:
            raise serializers.ValidationError("No active amendment found.")
        validated_data['imdgamendment'] = lookup_service.active_amendment
        
        try:
            return super().create(validated_data)
        except IntegrityError as e:
            raise serializers.ValidationError({
                'code': ['This code already exists in the current amendment.']
            }) from e

class PackingInstructionsSerializer(serializers.ModelSerializer):
    """Custom serializer for PackingInstructions model with bulk creation support."""
    class Meta:
        model = PackingInstructions
        fields = ['id',
                  'code',
                  'file',
                  'description']
        list_serializer_class = BaseListSerializer

    def create(self, validated_data):
        lookup_service = IMDGLookupService()
        if not lookup_service.active_amendment:
            raise serializers.ValidationError("No active amendment found.")
        validated_data['imdgamendment'] = lookup_service.active_amendment
        
        try:
            return super().create(validated_data)
        except IntegrityError as e:
            raise serializers.ValidationError({
                'code': ['This code already exists in the current amendment.']
            }) from e


class PackingProvisionsSerializer(serializers.ModelSerializer):
    """Custom serializer for PackingProvisions model with bulk creation support."""
    class Meta:
        model = PackingProvisions
        fields = ['id',
                  'code',
                  'file',
                  'description']
        list_serializer_class = BaseListSerializer

    def create(self, validated_data):
        lookup_service = IMDGLookupService()
        if not lookup_service.active_amendment:
            raise serializers.ValidationError("No active amendment found.")
        validated_data['imdgamendment'] = lookup_service.active_amendment
        
        try:
            return super().create(validated_data)
        except IntegrityError as e:
            raise serializers.ValidationError({
                'code': ['This code already exists in the current amendment.']
            }) from e


class IBCInstructionsSerializer(serializers.ModelSerializer):
    """Custom serializer for IBCInstructions model with bulk creation support."""
    class Meta:
        model = IBCInstructions
        fields = ['id',
                  'code',
                  'file',
                  'description']
        list_serializer_class = BaseListSerializer

    def create(self, validated_data):
        lookup_service = IMDGLookupService()
        if not lookup_service.active_amendment:
            raise serializers.ValidationError("No active amendment found.")
        validated_data['imdgamendment'] = lookup_service.active_amendment
        
        try:
            return super().create(validated_data)
        except IntegrityError as e:
            raise serializers.ValidationError({
                'code': ['This code already exists in the current amendment.']
            }) from e

class IBCProvisionsSerializer(serializers.ModelSerializer):
    """Custom serializer for IBCProvisions model with bulk creation support."""
    class Meta:
        model = IBCProvisions
        fields = ['id',
                  'code',
                  'file',
                  'description']
        list_serializer_class = BaseListSerializer

    def create(self, validated_data):
        lookup_service = IMDGLookupService()
        if not lookup_service.active_amendment:
            raise serializers.ValidationError("No active amendment found.")
        validated_data['imdgamendment'] = lookup_service.active_amendment
        
        try:
            return super().create(validated_data)
        except IntegrityError as e:
            raise serializers.ValidationError({
                'code': ['This code already exists in the current amendment.']
            }) from e
    

class TankInstructionsSerializer(serializers.ModelSerializer):
    """Custom serializer for Tank Instructions model with bulk creation support."""
    class Meta:
        model = TankInstructions
        fields = ['id',
                  'code',
                  'file',
                  'description']
        list_serializer_class = BaseListSerializer

    def create(self, validated_data):
        lookup_service = IMDGLookupService()
        if not lookup_service.active_amendment:
            raise serializers.ValidationError("No active amendment found.")
        validated_data['imdgamendment'] = lookup_service.active_amendment
        
        try:
            return super().create(validated_data)
        except IntegrityError as e:
            raise serializers.ValidationError({
                'code': ['This code already exists in the current amendment.']
            }) from e
    

class TankProvisionsSerializer(serializers.ModelSerializer):
    """Custom serializer for Tank Provisions model with bulk creation support."""
    imdg_amendment_id = serializers.PrimaryKeyRelatedField(
        queryset=IMDGAmendment.objects.all(),
        source='imdgamendment',
        write_only=True
    )
    class Meta:
        model = TankProvisions
        fields = ['id',
                  'code',
                  'file',
                  'description']
        list_serializer_class = BaseListSerializer

    def create(self, validated_data):
        lookup_service = IMDGLookupService()
        if not lookup_service.active_amendment:
            raise serializers.ValidationError("No active amendment found.")
        validated_data['imdgamendment'] = lookup_service.active_amendment
        
        try:
            return super().create(validated_data)
        except IntegrityError as e:
            raise serializers.ValidationError({
                'code': ['This code already exists in the current amendment.']
            }) from e


class EmergencySchedulesSerializer(serializers.ModelSerializer):
    """Custom serializer for Emergency SChedule model with bulk creation support."""
    class Meta:
        model = EmergencySchedules
        fields = ['id',
                  'code',
                  'file',
                  'description']
        list_serializer_class = BaseListSerializer

    def create(self, validated_data):
        lookup_service = IMDGLookupService()
        if not lookup_service.active_amendment:
            raise serializers.ValidationError("No active amendment found.")
        validated_data['imdgamendment'] = lookup_service.active_amendment
        
        try:
            return super().create(validated_data)
        except IntegrityError as e:
            raise serializers.ValidationError({
                'code': ['This code already exists in the current amendment.']
            }) from e
    

class StowageHandlingSerializer(serializers.ModelSerializer):
    """Custom serializer for Stowage Handling model with bulk creation support."""
    class Meta:
        model = StowageHandling
        fields = ['id',
                  'code',
                  'file',
                  'description']
        list_serializer_class = BaseListSerializer

    def create(self, validated_data):
        lookup_service = IMDGLookupService()
        if not lookup_service.active_amendment:
            raise serializers.ValidationError("No active amendment found.")
        validated_data['imdgamendment'] = lookup_service.active_amendment
        
        try:
            return super().create(validated_data)
        except IntegrityError as e:
            raise serializers.ValidationError({
                'code': ['This code already exists in the current amendment.']
            }) from e
    
class SegregationSerializer(serializers.ModelSerializer):
    """Custom serializer for SpecialProvisions model with bulk creation support."""
    class Meta:
        model = Segregation
        fields = ['id',
                  'code',
                  'file',
                  'description']
        list_serializer_class = BaseListSerializer

    def create(self, validated_data):
        lookup_service = IMDGLookupService()
        if not lookup_service.active_amendment:
            raise serializers.ValidationError("No active amendment found.")
        validated_data['imdgamendment'] = lookup_service.active_amendment
        
        try:
            return super().create(validated_data)
        except IntegrityError as e:
            raise serializers.ValidationError({
                'code': ['This code already exists in the current amendment.']
            }) from e

class SegregationRuleSerializer(serializers.ModelSerializer):
    """Custom serializer for SegregationBar model."""
    from_class_code = serializers.SlugRelatedField(
        slug_field='code',
        queryset=ClassDivision.objects.all(),
        source='fromclass'
    )
    to_class_code = serializers.SlugRelatedField(
        slug_field='code',
        queryset=ClassDivision.objects.all(),
        source='toclass'
    )
    from_class = ClassDivisionSerializer(
        read_only=True, 
        source='fromclass'
    )
    to_class = ClassDivisionSerializer(
        read_only=True, 
        source='toclass'
    )
    class Meta:
        model = SegregationRule
        fields = ['id',
                  'from_class_code', 'from_class',
                  'to_class_code', 'to_class',
                  'requirement']
        list_serializer_class = BaseListSerializer

    def validate(self, data):
        from_class_instance = data.get('fromclass')
        to_class_instance = data.get('toclass')
        
        lookup_service = IMDGLookupService()
        active_amendment = lookup_service.active_amendment

        if not active_amendment:
             raise serializers.ValidationError("No active amendment found for validation.")
        
        existing_rule = SegregationRule.objects.filter(
            imdgamendment=active_amendment,
            fromclass=from_class_instance,
            toclass=to_class_instance
        ).exists()
        
        if existing_rule:
            raise serializers.ValidationError(
                "Segregation rule for this combination already exists in the active amendment."
            )
        
        return data
    
    def create(self, validated_data):
        lookup_service = IMDGLookupService()
        if not lookup_service.active_amendment:
            raise serializers.ValidationError("No active amendment found.")
        validated_data['imdgamendment'] = lookup_service.active_amendment
        return super().create(validated_data)

class DangerousGoodsSerializer(serializers.ModelSerializer):
    """Custom serializer for DangerousGoods model."""
    class Meta:
        model = DangerousGoods
        fields = ['id',
                  'un_code',
                  'proper_shipping_name',
                  'class_division_code',
                  'subsidiary_hazards_codes',
                  'packing_group_code',
                  'special_provisions_codes',
                  'limited_quantities',
                  'excepted_quantities_codes',
                  'packing_instructions_codes',
                  'packing_provisions_codes',
                  'ibc_instructions_codes',
                  'ibc_provisions_codes',
                  'tank_instructions_codes',
                  'tank_provisions_codes',
                  'emergency_schedules_codes',
                  'stowage_handling_codes',
                  'segregation_codes',
                  'observations',
                  ]
        list_serializer_class = BaseListSerializer

    def to_representation(self, instance):  
        representation = super().to_representation(instance)
        view = self.context.get('view')

        if view and view.action == 'retrieve':
            lookup_service = IMDGLookupService()
            computed_data = lookup_service.get_computed_details(instance)
            representation.update(computed_data)

        return representation
    
    def create(self, validated_data):
        lookup_service = IMDGLookupService()
        if not lookup_service.active_amendment:
            raise serializers.ValidationError("No active amendment found.")
        validated_data['imdgamendment'] = lookup_service.active_amendment
        return super().create(validated_data)


