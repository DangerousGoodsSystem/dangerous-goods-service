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

class BaseListSerializer(serializers.ListSerializer):
    """
    Custom ListSerializer to handle bulk creation with detailed error reporting.
    """
    def create(self, validated_data):
        instances = []
        errors = []
        for idx, item_data in enumerate(validated_data):
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


class IMDGAmendmentSerializer(serializers.ModelSerializer):
    """Serializer for IMDGAmendment model."""
    class Meta:
        model = IMDGAmendment
        fields = ['id',
                  'name',
                  'is_effective',
                  'upload_at']
        list_serializer_class = BaseListSerializer


class UNCodeSerializer(serializers.ModelSerializer):
    """Custom serializer for UNCode model with bulk creation support."""
    imdg_amendment_id = serializers.PrimaryKeyRelatedField(
        queryset=IMDGAmendment.objects.all(),
        source='imdgamendment',
        write_only=True
    )
    class Meta:
        model = UNCode
        fields = ['id',
                  'imdg_amendment_id',
                  'code',
                  'description']
        list_serializer_class = BaseListSerializer


class ClassDivisionSerializer(serializers.ModelSerializer):
    """Custom serializer for Classification model with bulk creation support."""
    imdg_amendment_id = serializers.PrimaryKeyRelatedField(
        queryset=IMDGAmendment.objects.all(),
        source='imdgamendment',
        write_only=True
    )
    class Meta:
        model = ClassDivision
        fields = ['id',
                  'imdg_amendment_id',
                  'code',
                  'label',
                  'description']
        list_serializer_class = BaseListSerializer


class PackingGroupSerializer(serializers.ModelSerializer):
    """Custom serializer for PackingGroup model with bulk creation support."""
    imdg_amendment_id = serializers.PrimaryKeyRelatedField(
        queryset=IMDGAmendment.objects.all(),
        source='imdgamendment',
        write_only=True
    )
    class Meta:
        model = PackingGroup
        fields = ['id',
                  'imdg_amendment_id',
                  'code',
                  'file',
                  'description',
                  ]
        list_serializer_class = BaseListSerializer


class SpecialProvisionsSerializer(serializers.ModelSerializer):
    """Custom serializer for SpecialProvisions model with bulk creation support."""
    imdg_amendment_id = serializers.PrimaryKeyRelatedField(
        queryset=IMDGAmendment.objects.all(),
        source='imdgamendment',
        write_only=True
    )
    class Meta:
        model = SpecialProvisions
        fields = ['id',
                  'imdg_amendment_id',
                  'code',
                  'file',
                  'description']
        list_serializer_class = BaseListSerializer


class ExceptedQuantitiesSerializer(serializers.ModelSerializer):
    """Custom serializer for ExceptedQuantities model with bulk creation support."""
    imdg_amendment_id = serializers.PrimaryKeyRelatedField(
        queryset=IMDGAmendment.objects.all(),
        source='imdgamendment',
        write_only=True
    )
    class Meta:
        model = ExceptedQuantities
        fields = ['id',
                  'imdg_amendment_id',
                  'code',
                  'file',
                  'description']
        list_serializer_class = BaseListSerializer

class PackingInstructionsSerializer(serializers.ModelSerializer):
    """Custom serializer for PackingInstructions model with bulk creation support."""
    imdg_amendment_id = serializers.PrimaryKeyRelatedField(
        queryset=IMDGAmendment.objects.all(),
        source='imdgamendment',
        write_only=True
    )
    class Meta:
        model = PackingInstructions
        fields = ['id',
                  'imdg_amendment_id',
                  'code',
                  'file',
                  'description']
        list_serializer_class = BaseListSerializer


class PackingProvisionsSerializer(serializers.ModelSerializer):
    """Custom serializer for PackingProvisions model with bulk creation support."""
    imdg_amendment_id = serializers.PrimaryKeyRelatedField(
        queryset=IMDGAmendment.objects.all(),
        source='imdgamendment',
        write_only=True
    )
    class Meta:
        model = PackingProvisions
        fields = ['id',
                  'imdg_amendment_id',
                  'code',
                  'file',
                  'description']
        list_serializer_class = BaseListSerializer


class IBCInstructionsSerializer(serializers.ModelSerializer):
    """Custom serializer for IBCInstructions model with bulk creation support."""
    imdg_amendment_id = serializers.PrimaryKeyRelatedField(
        queryset=IMDGAmendment.objects.all(),
        source='imdgamendment',
        write_only=True
    )
    class Meta:
        model = IBCInstructions
        fields = ['id',
                  'imdg_amendment_id',
                  'code',
                  'file',
                  'description']
        list_serializer_class = BaseListSerializer


class IBCProvisionsSerializer(serializers.ModelSerializer):
    """Custom serializer for IBCProvisions model with bulk creation support."""
    imdg_amendment_id = serializers.PrimaryKeyRelatedField(
        queryset=IMDGAmendment.objects.all(),
        source='imdgamendment',
        write_only=True
    )
    class Meta:
        model = IBCProvisions
        fields = ['id',
                  'imdg_amendment_id',
                  'code',
                  'file',
                  'description']
        list_serializer_class = BaseListSerializer
    

class TankInstructionsSerializer(serializers.ModelSerializer):
    """Custom serializer for Tank Instructions model with bulk creation support."""
    imdg_amendment_id = serializers.PrimaryKeyRelatedField(
        queryset=IMDGAmendment.objects.all(),
        source='imdgamendment',
        write_only=True
    )
    class Meta:
        model = TankInstructions
        fields = ['id',
                  'imdg_amendment_id',
                  'code',
                  'file',
                  'description']
        list_serializer_class = BaseListSerializer
    

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
                  'imdg_amendment_id',
                  'code',
                  'file',
                  'description']
        list_serializer_class = BaseListSerializer


class EmergencySchedulesSerializer(serializers.ModelSerializer):
    """Custom serializer for Emergency SChedule model with bulk creation support."""
    imdg_amendment_id = serializers.PrimaryKeyRelatedField(
        queryset=IMDGAmendment.objects.all(),
        source='imdgamendment',
        write_only=True
    )
    class Meta:
        model = EmergencySchedules
        fields = ['id',
                  'imdg_amendment_id',
                  'code',
                  'file',
                  'description']
        list_serializer_class = BaseListSerializer
    

class StowageHandlingSerializer(serializers.ModelSerializer):
    """Custom serializer for Stowage Handling model with bulk creation support."""
    imdg_amendment_id = serializers.PrimaryKeyRelatedField(
        queryset=IMDGAmendment.objects.all(),
        source='imdgamendment',
        write_only=True
    )
    class Meta:
        model = StowageHandling
        fields = ['id',
                  'imdg_amendment_id',
                  'code',
                  'file',
                  'description']
        list_serializer_class = BaseListSerializer
    

class SegregationSerializer(serializers.ModelSerializer):
    """Custom serializer for SpecialProvisions model with bulk creation support."""
    imdg_amendment_id = serializers.PrimaryKeyRelatedField(
        queryset=IMDGAmendment.objects.all(),
        source='imdgamendment',
        write_only=True
    )
    class Meta:
        model = Segregation
        fields = ['id',
                  'imdg_amendment_id',
                  'code',
                  'file',
                  'description']
        list_serializer_class = BaseListSerializer

class SegregationRuleSerializer(serializers.ModelSerializer):
    """Custom serializer for SegregationBar model."""
    imdg_amendment_id = serializers.PrimaryKeyRelatedField(
        queryset=IMDGAmendment.objects.all(),
        source='imdgamendment',
        write_only=True
    )
    from_class_id = serializers.PrimaryKeyRelatedField(
        queryset=ClassDivision.objects.all(),
        source='fromclass',
        write_only=True
    )
    to_class_id = serializers.PrimaryKeyRelatedField(
        queryset=ClassDivision.objects.all(),
        source='toclass',
        write_only=True
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
                  'imdg_amendment_id',
                  'from_class_id', 'from_class',
                  'to_class_id', 'to_class',
                  'requirement']
        list_serializer_class = BaseListSerializer

    def validate(self, data):
        existing_rule = SegregationRule.objects.filter(
            imdgamendment=data.get('imdgamendment'),
            fromclass=data.get('fromclass'),
            toclass=data.get('toclass')
        ).exists()
        if existing_rule:
            raise serializers.ValidationError(
                "Segregation rule for this combination already exists."
            )
        
        return data

class DangerousGoodsSerializer(serializers.ModelSerializer):
    """Custom serializer for DangerousGoods model."""
    imdg_amendment_id = serializers.PrimaryKeyRelatedField(
        queryset=IMDGAmendment.objects.all(),
        source='imdgamendment',
        write_only=True
    )
    class Meta:
        model = DangerousGoods
        fields = ['id',
                  'imdg_amendment_id',
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


