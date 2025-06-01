from rest_framework import serializers
from django.db import IntegrityError
from .helpers import get_or_create_class_division_group
from .models import (
    UNCode, UNCodeImage,
    Classification,
    Division,
    CompatibilityGroup,
    ClassDivisionGroup,
    PackingGroup, PackingGroupImage,
    SpecialProvisions, SpecialProvisionsImage,
    ExceptedQuantities, ExceptedQuantitiesImage,
    PackingInstructions, PackingInstructionsImage,
    PackingProvisions, PackingProvisionsImage,
    IBCInstructions, IBCInstructionsImage,
    IBCProvisions, IBCProvisionsImage,
    TankInstructions, TankInstructionsImage,
    TankProvisions, TankProvisionsImage,
    EmergencySchedule, EmergencyScheduleImage,
    StowageHandling, StowageHandlingImage,
    Segregation, SegregationImage,
    SegregationBar,
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

class UNCodeImageSerializer(serializers.ModelSerializer):
    """Serializer for UNCodeImage model."""
    un_code_id = serializers.PrimaryKeyRelatedField(
        queryset=UNCode.objects.filter(activate=True),
        source='uncode',
        write_only=True
    )
    class Meta:
        model = UNCodeImage
        fields = ['id', 'un_code_id', 'image']

class PackingGroupImageSerializer(serializers.ModelSerializer):
    """Serializer for PackingGroupImage model."""
    packing_group_id = serializers.PrimaryKeyRelatedField(
        queryset=PackingGroup.objects.filter(activate=True),
        source='packinggroup',
        write_only=True
    )
    class Meta:
        model = PackingGroupImage
        fields = ['id', 'packing_group_id', 'image']

class SpecialProvisionsImageSerializer(serializers.ModelSerializer):
    """Serializer for SpecialProvisionsImage model."""
    special_provisions_id = serializers.PrimaryKeyRelatedField(
        queryset=SpecialProvisions.objects.filter(activate=True),
        source='specialprovisions',
        write_only=True
    )
    class Meta:
        model = SpecialProvisionsImage
        fields = ['id', 'special_provisions_id', 'image']

class ExceptedQuantitiesImageSerializer(serializers.ModelSerializer):
    """Serializer for ExceptedQuantitiesImage model."""
    excepted_quantities_id = serializers.PrimaryKeyRelatedField(
        queryset=ExceptedQuantities.objects.filter(activate=True),
        source='exceptedquantities',
        write_only=True
    )
    class Meta:
        model = ExceptedQuantitiesImage
        fields = ['id', 'excepted_quantities_id', 'image']

class PackingInstructionsImageSerializer(serializers.ModelSerializer):
    """Serializer for PackingInstructionsImage model."""
    packing_instructions_id = serializers.PrimaryKeyRelatedField(
        queryset=PackingInstructions.objects.filter(activate=True),
        source='packinginstructions',
        write_only=True
    )
    class Meta:
        model = PackingInstructionsImage
        fields = ['id', 'packing_instructions_id', 'image']

class PackingProvisionsImageSerializer(serializers.ModelSerializer):
    """Serializer for PackingProvisionsImage model."""
    packing_provisions_id = serializers.PrimaryKeyRelatedField(
        queryset=PackingProvisions.objects.filter(activate=True),
        source='packingprovisions',
        write_only=True
    )
    class Meta:
        model = PackingProvisionsImage
        fields = ['id', 'packing_provisions_id', 'image']

class IBCInstructionsImageSerializer(serializers.ModelSerializer):
    """Serializer for IBCInstructionsImage model."""
    ibc_instructions_id = serializers.PrimaryKeyRelatedField(
        queryset=IBCInstructions.objects.filter(activate=True),
        source='ibcinstructions',
        write_only=True
    )
    class Meta:
        model = IBCInstructionsImage
        fields = ['id', 'ibc_instructions_id', 'image']

class IBCProvisionsImageSerializer(serializers.ModelSerializer):
    """Serializer for IBCProvisionsImage model."""
    ibc_provisions_id = serializers.PrimaryKeyRelatedField(
        queryset=IBCProvisions.objects.filter(activate=True),
        source='ibcprovisions',
        write_only=True
    )
    class Meta:
        model = IBCProvisionsImage
        fields = ['id', 'ibc_provisions_id', 'image']

class TankInstructionsImageSerializer(serializers.ModelSerializer):
    """Serializer for TankInstructionsImage model."""
    tank_instructions_id = serializers.PrimaryKeyRelatedField(
        queryset=TankInstructions.objects.filter(activate=True),
        source='tankinstructions',
        write_only=True
    )
    class Meta:
        model = TankInstructionsImage
        fields = ['id', 'tank_instructions_id', 'image']

class TankProvisionsImageSerializer(serializers.ModelSerializer):
    """Serializer for TankProvisionsImage model."""
    tank_provisions_id = serializers.PrimaryKeyRelatedField(
        queryset=TankProvisions.objects.filter(activate=True),
        source='tankprovisions',
        write_only=True
    )
    class Meta:
        model = TankProvisionsImage
        fields = ['id', 'tank_provisions_id', 'image']

class EmergencyScheduleImageSerializer(serializers.ModelSerializer):
    """Serializer for EmergencyScheduleImage model."""
    emergency_schedule_id = serializers.PrimaryKeyRelatedField(
        queryset=EmergencySchedule.objects.filter(activate=True),
        source='emergencyschedule',
        write_only=True
    )
    class Meta:
        model = EmergencyScheduleImage
        fields = ['id', 'emergency_schedule_id', 'image']

class StowageHandlingImageSerializer(serializers.ModelSerializer):
    """Serializer for StowageHandlingImage model."""
    stowage_handling_id = serializers.PrimaryKeyRelatedField(
        queryset=StowageHandling.objects.filter(activate=True),
        source='stowagehandling',
        write_only=True
    )
    class Meta:
        model = StowageHandlingImage
        fields = ['id', 'stowage_handling_id', 'image']

class SegregationImageSerializer(serializers.ModelSerializer):
    """Serializer for SegregationImage model."""
    segregation_id = serializers.PrimaryKeyRelatedField(
        queryset=Segregation.objects.filter(activate=True),
        source='segregation',
        write_only=True
    )
    class Meta:
        model = SegregationImage
        fields = ['id', 'segregation_id', 'image']

class UNCodeSerializer(serializers.ModelSerializer):
    """Custom serializer for UNCode model with bulk creation support."""
    images = UNCodeImageSerializer(many=True, read_only=True)
    class Meta:
        model = UNCode
        fields = ['id',
                  'code',
                  'images',
                  'description']
        extra_kwargs = {
        'code': {'validators': []}
        }
        list_serializer_class = BaseListSerializer

    def create(self, validated_data):
        code = validated_data.get('code')
        instance = UNCode.objects.filter(code=code).first()
        if instance:
            if not instance.activate:
                instance.activate = True
                instance.description = validated_data.get('description')
                instance.save()
                return instance
            else:
                raise serializers.ValidationError({'error': f'Code {code} has existed'})
        return super().create(validated_data)

class ClassificationSerializer(serializers.ModelSerializer):
    """Custom serializer for Classification model with bulk creation support."""
    class Meta:
        model = Classification
        fields = ['id',
                  'code',
                  'label', 'description']
        extra_kwargs = {
        'code': {'validators': []}
        }
        list_serializer_class = BaseListSerializer

    def create(self, validated_data):
        code = validated_data.get('code')
        instance = Classification.objects.filter(code=code).first()
        if instance:
            if not instance.activate:
                instance.activate = True
                instance.label = validated_data.get('label')
                instance.description = validated_data.get('description')
                instance.save()
                return instance
            else:
                raise serializers.ValidationError({'error': f'Code {code} has existed'})
        return super().create(validated_data)


class DivisionSerializer(serializers.ModelSerializer):
    """Custom serializer for Division model with bulk creation support."""
    classification_id = serializers.PrimaryKeyRelatedField(
        queryset=Classification.objects.all(),
        source='classification',
        write_only=True
    )
    classification = ClassificationSerializer(read_only=True)

    class Meta:
        model = Division
        fields = ['id',
                  'classification_id', 'classification',
                  'code',
                  'label', 'description']
        extra_kwargs = {
        'classification_id': {'validators': []},
        'code': {'validators': []}
        }
        list_serializer_class = BaseListSerializer

    def create(self, validated_data):
        classification_id = validated_data.get('classification_id')
        code = validated_data.get('code')
        instance = Division.objects.filter(classification_id=classification_id, code=code).first()
        if instance:
            if not instance.activate:
                instance.activate = True
                instance.label = validated_data.get('label')
                instance.description = validated_data.get('description')
                instance.save()
                return instance
            else:
                raise serializers.ValidationError({'error': f'Code {code} has existed'})  
        return super().create(validated_data)


class CompatibilityGroupSerializer(serializers.ModelSerializer):
    """Custom serializer for CompatibilityGroup model with bulk creation support."""
    division_id = serializers.PrimaryKeyRelatedField(
        queryset=Division.objects.all(),
        source='division',
        write_only=True
    )
    division = DivisionSerializer(read_only=True)

    class Meta:
        model = CompatibilityGroup
        fields = ['id',
                  'division_id', 'division',
                  'code',
                  'description']
        extra_kwargs = {
        'division_id': {'validators': []},
        'code': {'validators': []}
        }
        list_serializer_class = BaseListSerializer

    def create(self, validated_data):
        division_id = validated_data.get('division_id')
        code = validated_data.get('code')
        instance = CompatibilityGroup.objects.filter(division_id=division_id, code=code).first()
        if instance:
            if not instance.activate:
                instance.activate = True
                instance.description = validated_data.get('description')
                instance.save()
                return instance
            else:
                raise serializers.ValidationError({'error': f'Code {code} has existed'})
        return super().create(validated_data)

class ClassDivisionGroupField(serializers.Field):
    """
    Custom Field to map code string --> ClassDivisionGroup instance.
    """
    def to_representation(self, obj: ClassDivisionGroup):
        s = obj.classification.code
        if obj.division:
            s += f".{obj.division.code}"
        if obj.compatibility_group:
            s += obj.compatibility_group.code
        return s

    def to_internal_value(self, data):
        if not isinstance(data, str):
            raise serializers.ValidationError("Must pass a string like '2', '2.1' or '1.1A'.")
        try:
            instance, created = get_or_create_class_division_group(data)
        except ValueError as e:
            raise serializers.ValidationError(str(e))
        return instance

class ClassDivisionGroupListField(serializers.ListField):
    """
    Custom ListField to handle a list of ClassDivisionGroup instances.
    """
    def __init__(self, **kwargs):
        super().__init__(child=ClassDivisionGroupField(), **kwargs)

    def to_representation(self, data):
        if hasattr(data, 'all'):
            data = data.all()
        return super().to_representation(data)

class PackingGroupSerializer(serializers.ModelSerializer):
    """Custom serializer for PackingGroup model with bulk creation support."""
    images = PackingGroupImageSerializer(many=True, read_only=True)
    class Meta:
        model = PackingGroup
        fields = ['id',
                  'code',
                  'images',
                  'description',
                  ]
        extra_kwargs = {
        'code': {'validators': []}
        }
        list_serializer_class = BaseListSerializer
    def create(self, validated_data):
        code = validated_data.get('code')
        instance = PackingGroup.objects.filter(code=code).first()
        if instance:
            if not instance.activate:
                instance.activate = True
                instance.description = validated_data.get('description')
                instance.save()
                return instance
            else:
                raise serializers.ValidationError({'error': f'Code {code} has existed'})
        return super().create(validated_data)

class SpecialProvisionsSerializer(serializers.ModelSerializer):
    """Custom serializer for SpecialProvisions model with bulk creation support."""
    images = SpecialProvisionsImageSerializer(many=True, read_only=True)
    class Meta:
        model = SpecialProvisions
        fields = ['id',
                  'code',
                  'images',
                  'description']
        extra_kwargs = {
        'code': {'validators': []}
        }
        list_serializer_class = BaseListSerializer

    def create(self, validated_data):
            code = validated_data.get('code')
            instance = SpecialProvisions.objects.filter(code=code).first()
            if instance:
                if not instance.activate:
                    instance.activate = True
                    instance.description = validated_data.get('description')
                    instance.save()
                    return instance
                else:
                    raise serializers.ValidationError({'error': f'Code {code} has existed'})
            return super().create(validated_data)   

class ExceptedQuantitiesSerializer(serializers.ModelSerializer):
    """Custom serializer for ExceptedQuantities model with bulk creation support."""
    images = ExceptedQuantitiesImageSerializer(many=True, read_only=True)
    class Meta:
        model = ExceptedQuantities
        fields = ['id',
                  'code',
                  'images',
                  'description']
        extra_kwargs = {
        'code': {'validators': []}
        }
        list_serializer_class = BaseListSerializer

    def create(self, validated_data):
        code = validated_data.get('code')
        instance = ExceptedQuantities.objects.filter(code=code).first()
        if instance:
            if not instance.activate:
                instance.activate = True
                instance.description = validated_data.get('description')
                instance.save()
                return instance
            else:
                raise serializers.ValidationError({'error': f'Code {code} has existed'})
        return super().create(validated_data)

class PackingInstructionsSerializer(serializers.ModelSerializer):
    """Custom serializer for PackingInstructions model with bulk creation support."""
    images = PackingInstructionsImageSerializer(many=True, read_only=True)
    class Meta:
        model = PackingInstructions
        fields = ['id',
                  'code',
                  'images',
                  'description']
        extra_kwargs = {
        'code': {'validators': []}
        }
        list_serializer_class = BaseListSerializer

    def create(self, validated_data):
        code = validated_data.get('code')
        instance = PackingInstructions.objects.filter(code=code).first()
        if instance:
            if not instance.activate:
                instance.activate = True
                instance.description = validated_data.get('description')
                instance.save()
                return instance
            else:
                raise serializers.ValidationError({'error': f'Code {code} has existed'})
        return super().create(validated_data)

class PackingProvisionsSerializer(serializers.ModelSerializer):
    """"Custom serializer for PackingProvisions model with bulk creation support."""
    images = PackingProvisionsImageSerializer(many=True, read_only=True)
    class Meta:
        model = PackingProvisions
        fields = ['id',
                  'code',
                  'images',
                  'description']
        extra_kwargs = {
        'code': {'validators': []}
        }
        list_serializer_class = BaseListSerializer

    def create(self, validated_data):
        code = validated_data.get('code')
        instance = PackingProvisions.objects.filter(code=code).first()
        if instance:
            if not instance.activate:
                instance.activate = True
                instance.description = validated_data.get('description')
                instance.save()
                return instance
            else:
                raise serializers.ValidationError({'error': f'Code {code} has existed'})
        return super().create(validated_data)

class IBCInstructionsSerializer(serializers.ModelSerializer):
    """Custom serializer for IBCInstructions model with bulk creation support."""
    images = IBCInstructionsImageSerializer(many=True, read_only=True)
    class Meta:
        model = IBCInstructions
        fields = ['id',
                  'code',
                  'images',
                  'description']
        extra_kwargs = {
        'code': {'validators': []}
        }
        list_serializer_class = BaseListSerializer

    def create(self, validated_data):
        code = validated_data.get('code')
        instance = IBCInstructions.objects.filter(code=code).first()
        if instance:
            if not instance.activate:
                instance.activate = True
                instance.description = validated_data.get('description')
                instance.save()
                return instance
            else:
                raise serializers.ValidationError({'error': f'Code {code} has existed'})
        return super().create(validated_data)

class IBCProvisionsSerializer(serializers.ModelSerializer):
    """Custom serializer for IBCProvisions model with bulk creation support."""
    images = IBCProvisionsImageSerializer(many=True, read_only=True)
    class Meta:
        model = IBCProvisions
        fields = ['id',
                  'code',
                  'images',
                  'description']
        extra_kwargs = {
        'code': {'validators': []}
        }
        list_serializer_class = BaseListSerializer

    def create(self, validated_data):
        code = validated_data.get('code')
        instance = IBCProvisions.objects.filter(code=code).first()
        if instance:
            if not instance.activate:
                instance.activate = True
                instance.description = validated_data.get('description')
                instance.save()
                return instance
            else:
                raise serializers.ValidationError({'error': f'Code {code} has existed'})
        return super().create(validated_data)

class TankInstructionsSerializer(serializers.ModelSerializer):
    """Custom serializer for TankInstructions model with bulk creation support."""
    images = TankInstructionsImageSerializer(many=True, read_only=True)
    class Meta:
        model = TankInstructions
        fields = ['id',
                  'code',
                  'images',
                  'description']
        extra_kwargs = {
        'code': {'validators': []}
        }
        list_serializer_class = BaseListSerializer

    def create(self, validated_data):
        code = validated_data.get('code')
        instance = TankInstructions.objects.filter(code=code).first()
        if instance:
            if not instance.activate:
                instance.activate = True
                instance.description = validated_data.get('description')
                instance.save()
                return instance
            else:
                raise serializers.ValidationError({'error': f'Code {code} has existed'})
        return super().create(validated_data)

class TankProvisionsSerializer(serializers.ModelSerializer):
    """Custom serializer for TankProvisions model with bulk creation support."""
    images = TankProvisionsImageSerializer(many=True, read_only=True)
    class Meta:
        model = TankProvisions
        fields = ['id',
                  'code',
                  'images',
                  'description']
        extra_kwargs = {
        'code': {'validators': []}
        }
        list_serializer_class = BaseListSerializer

    def create(self, validated_data):
        code = validated_data.get('code')
        instance = TankProvisions.objects.filter(code=code).first()
        if instance:
            if not instance.activate:
                instance.activate = True
                instance.description = validated_data.get('description')
                instance.save()
                return instance
            else:
                raise serializers.ValidationError({'error': f'Code {code} has existed'})
        return super().create(validated_data)

class EmergencyScheduleSerializer(serializers.ModelSerializer):
    """Custom serializer for EmergencySchedule model with bulk creation support."""
    images = EmergencyScheduleImageSerializer(many=True, read_only=True)
    class Meta:
        model = EmergencySchedule
        fields = ['id',
                  'code',
                  'images',
                  'description']
        extra_kwargs = {
        'code': {'validators': []}
        }
        list_serializer_class = BaseListSerializer

    def create(self, validated_data):
        code = validated_data.get('code')
        instance = EmergencySchedule.objects.filter(code=code).first()
        if instance:
            if not instance.activate:
                instance.activate = True
                instance.description = validated_data.get('description')
                instance.save()
                return instance
            else:
                raise serializers.ValidationError({'error': f'Code {code} has existed'})
        return super().create(validated_data)

class StowageHandlingSerializer(serializers.ModelSerializer):
    """Custom serializer for StowageHandling model with bulk creation support."""
    images = StowageHandlingImageSerializer(many=True, read_only=True)
    class Meta:
        model = StowageHandling
        fields = ['id',
                  'code',
                  'images',
                  'description']
        extra_kwargs = {
        'code': {'validators': []}
        }
        list_serializer_class = BaseListSerializer

    def create(self, validated_data):
        code = validated_data.get('code')
        instance = StowageHandling.objects.filter(code=code).first()
        if instance:
            if not instance.activate:
                instance.activate = True
                instance.description = validated_data.get('description')
                instance.save()
                return instance
            else:
                raise serializers.ValidationError({'error': f'Code {code} has existed'})
        return super().create(validated_data)

class SegregationSerializer(serializers.ModelSerializer):
    """Custom serializer for Segregation model with bulk creation support."""
    images = SegregationImageSerializer(many=True, read_only=True)
    class Meta:
        model = Segregation
        fields = ['id',
                  'code',
                  'images',
                  'description']
        extra_kwargs = {
        'code': {'validators': []}
        }
        list_serializer_class = BaseListSerializer

    def create(self, validated_data):
        code = validated_data.get('code')
        instance = Segregation.objects.filter(code=code).first()
        if instance:
            if not instance.activate:
                instance.activate = True
                instance.description = validated_data.get('description')
                instance.save()
                return instance
            else:
                raise serializers.ValidationError({'error': f'Code {code} has existed'})
        return super().create(validated_data)

class SegregationBarSerializer(serializers.ModelSerializer):
    """Custom serializer for SegregationBar model with bulk creation support."""
    from_class_id = serializers.PrimaryKeyRelatedField(
        queryset=ClassDivisionGroup.objects.all(),
        source='fromclass',
        write_only=True
    )
    to_class_id = serializers.PrimaryKeyRelatedField(
        queryset=ClassDivisionGroup.objects.all(),
        source='toclass',
        write_only=True
    )

    from_class = ClassDivisionGroupField(read_only=True)
    to_class = ClassDivisionGroupField(read_only=True)
    
    class Meta:
        model = SegregationBar
        fields = ['id',
                  'from_class_id', 'from_class',
                  'to_class_id', 'to_class',
                  'segregation_level']
        extra_kwargs = {
        'from_class_id': {'validators': []},
        'to_class_id': {'validators': []}
        }
        list_serializer_class = BaseListSerializer

    def create(self, validated_data):
        from_class_id = validated_data.get('from_class_id')
        to_class_id = validated_data.get('to_class_id')
        instance = SegregationBar.objects.filter(from_class_id=from_class_id, to_class_id=to_class_id).first()
        if instance:
            if not instance.activate:
                instance.activate = True
                instance.segregationlevel = validated_data.get('segregation_level')
                instance.save()
                return instance
            else:
                raise serializers.ValidationError({'error': 'from_class_id or to_class_id has existed'})
        return super().create(validated_data)


class DangerousGoodsSerializer(serializers.ModelSerializer):
    """Custom serializer for DangerousGoods model."""
    un_code_code = serializers.SlugRelatedField(
        slug_field='code',
        queryset=UNCode.objects.all(),
        source='uncode'
    )
    proper_shipping_name = serializers.CharField(
        source='propershippingname',
        allow_blank=True,
        allow_null=True,
        required=False
    )
    class_division_code = ClassDivisionGroupField(source='classdivision')
    subsidiary_hazards_codes = ClassDivisionGroupListField(
        source='subsidiaryhazards',
        required=False
    )
    packing_group_code = serializers.SlugRelatedField(
        slug_field='code',
        queryset=PackingGroup.objects.all(),
        source='packinggroup',
        required=False
    )
    special_provisions_codes = serializers.SlugRelatedField(
        many=True,
        slug_field='code',
        queryset=SpecialProvisions.objects.all(),
        source='specialprovisions',
        required=False
    )
    limited_quantities = serializers.CharField(
        source='limitedquantities',
        allow_blank=True,
        allow_null=True,
        required=False
    )
    excepted_quantities_codes = serializers.SlugRelatedField(
        many=True,
        slug_field='code',
        queryset=ExceptedQuantities.objects.all(),
        source='exceptedquantities',
        required=False
    )
    packing_instructions_codes = serializers.SlugRelatedField(
        many=True,
        slug_field='code',
        queryset=PackingInstructions.objects.all(),
        source='packinginstructions',
        required=False
    )
    packing_provisions_codes = serializers.SlugRelatedField(
        many=True,
        slug_field='code',
        queryset=PackingProvisions.objects.all(),
        source='packingprovisions',
        required=False
    )
    ibc_instructions_codes = serializers.SlugRelatedField(
        many=True,
        slug_field='code',
        queryset=IBCInstructions.objects.all(),
        source='ibcinstructions',
        required=False
    )
    ibc_provisions_codes = serializers.SlugRelatedField(
        many=True,
        slug_field='code',
        queryset=IBCProvisions.objects.all(),
        source='ibcprovisions',
        required=False
    )
    tank_instructions_codes = serializers.SlugRelatedField(
        many=True,
        slug_field='code',
        queryset=TankInstructions.objects.all(),
        source='tankinstructions',
        required=False
    )
    tank_provisions_codes = serializers.SlugRelatedField(
        many=True,
        slug_field='code',
        queryset=TankProvisions.objects.all(),
        source='tankprovisions',
        required=False
    )
    emergency_schedule_codes = serializers.SlugRelatedField(
        many=True,
        slug_field='code',
        queryset=EmergencySchedule.objects.all(),
        source='emergencyschedule',
        required=False
    )
    stowage_handling_codes = serializers.SlugRelatedField(
        many=True,
        slug_field='code',
        queryset=StowageHandling.objects.all(),
        source='stowagehandling',
        required=False
    )
    segregation_codes = serializers.SlugRelatedField(
        many=True,
        slug_field='code',
        queryset=Segregation.objects.all(),
        source='segregation',
        required=False
    )
    observations = serializers.CharField(required=False)

    class Meta:
        model = DangerousGoods
        fields = ['id',
                  'un_code_code',
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
                  'emergency_schedule_codes',
                  'stowage_handling_codes',
                  'segregation_codes',
                  'observations',
                  ]
        list_serializer_class = BaseListSerializer

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError as e:
            raise serializers.ValidationError({
                'non_field_errors': ['This combination already exists.']
            })