from django.conf import settings
from rest_framework import serializers
from .models import (
    IMDGAmendment,
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
    EmergencySchedules,
    StowageHandling,
    Segregation,
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
                  'file',
                  'name',
                  'upload_at',
                  'is_effective']
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

class ClassificationSerializer(serializers.ModelSerializer):
    """Custom serializer for Classification model with bulk creation support."""
    imdg_amendment_id = serializers.PrimaryKeyRelatedField(
        queryset=IMDGAmendment.objects.all(),
        source='imdgamendment',
        write_only=True
    )
    class Meta:
        model = Classification
        fields = ['id',
                  'imdg_amendment_id',
                  'code',
                  'label', 'description']
        list_serializer_class = BaseListSerializer


class DivisionSerializer(serializers.ModelSerializer):
    """Custom serializer for Division model with bulk creation support."""
    imdg_amendment_id = serializers.PrimaryKeyRelatedField(
        queryset=IMDGAmendment.objects.all(),
        source='imdgamendment',
        write_only=True
    )
    classification_id = serializers.PrimaryKeyRelatedField(
        queryset=Classification.objects.all(),
        source='classification',
        write_only=True
    )
    classification = ClassificationSerializer(read_only=True)

    class Meta:
        model = Division
        fields = ['id',
                  'imdg_amendment_id',
                  'classification_id', 'classification',
                  'code',
                  'label', 'description']
        list_serializer_class = BaseListSerializer

class CompatibilityGroupSerializer(serializers.ModelSerializer):
    """Custom serializer for CompatibilityGroup model with bulk creation support."""
    imdg_amendment_id = serializers.PrimaryKeyRelatedField(
        queryset=IMDGAmendment.objects.all(),
        source='imdgamendment',
        write_only=True
    )
    division_id = serializers.PrimaryKeyRelatedField(
        queryset=Division.objects.all(),
        source='division',
        write_only=True
    )
    division = DivisionSerializer(read_only=True)

    class Meta:
        model = CompatibilityGroup
        fields = ['id',
                  'imdg_amendment_id',
                  'division_id', 'division',
                  'code',
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
                  'pdf_regions',
                  'description',
                  ]
        list_serializer_class = BaseListSerializer

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        if not hasattr(instance, 'imdgamendment') or \
           not instance.imdgamendment or \
           not instance.imdgamendment.pages_directory_path:
            return representation

        pages_directory_path = instance.imdgamendment.pages_directory_path
        
        original_pdf_regions = representation.get('pdf_regions')

        if not isinstance(original_pdf_regions, list):
            return representation

        transformed_pdf_regions = []
        for region_data in original_pdf_regions:
            page_number = region_data.get('number_page') 
            coordinates = region_data.get('coordinates')

            if page_number is not None:
                media_url = settings.MEDIA_URL
                file_specific_path = f"{pages_directory_path}/{page_number}.pdf"
                link = f"{media_url}{file_specific_path}"
                
                transformed_pdf_regions.append({
                    'number_page': page_number,
                    'coordinates': coordinates,
                    'link_pdf': link
                    
                })
            else:
                transformed_pdf_regions.append(region_data) 
        
        representation['pdf_regions'] = transformed_pdf_regions
        return representation


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
                  'pdf_regions',
                  'description']
        list_serializer_class = BaseListSerializer

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        if not hasattr(instance, 'imdgamendment') or \
           not instance.imdgamendment or \
           not instance.imdgamendment.pages_directory_path:
            return representation

        pages_directory_path = instance.imdgamendment.pages_directory_path
        
        original_pdf_regions = representation.get('pdf_regions')

        if not isinstance(original_pdf_regions, list):
            return representation

        transformed_pdf_regions = []
        for region_data in original_pdf_regions:
            page_number = region_data.get('number_page') 
            coordinates = region_data.get('coordinates')

            if page_number is not None:
                media_url = settings.MEDIA_URL
                file_specific_path = f"{pages_directory_path}/{page_number}.pdf"
                link = f"{media_url}{file_specific_path}"
                
                transformed_pdf_regions.append({
                    'number_page': page_number,
                    'coordinates': coordinates,
                    'link_pdf': link
                    
                })
            else:
                transformed_pdf_regions.append(region_data) 
        
        representation['pdf_regions'] = transformed_pdf_regions
        return representation

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
                  'pdf_regions',
                  'description']
        list_serializer_class = BaseListSerializer

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        if not hasattr(instance, 'imdgamendment') or \
           not instance.imdgamendment or \
           not instance.imdgamendment.pages_directory_path:
            return representation

        pages_directory_path = instance.imdgamendment.pages_directory_path
        
        original_pdf_regions = representation.get('pdf_regions')

        if not isinstance(original_pdf_regions, list):
            return representation

        transformed_pdf_regions = []
        for region_data in original_pdf_regions:
            page_number = region_data.get('number_page') 
            coordinates = region_data.get('coordinates')

            if page_number is not None:
                media_url = settings.MEDIA_URL
                file_specific_path = f"{pages_directory_path}/{page_number}.pdf"
                link = f"{media_url}{file_specific_path}"
                
                transformed_pdf_regions.append({
                    'number_page': page_number,
                    'coordinates': coordinates,
                    'link_pdf': link
                    
                })
            else:
                transformed_pdf_regions.append(region_data) 
        
        representation['pdf_regions'] = transformed_pdf_regions
        return representation

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
                  'pdf_regions',
                  'description']
        list_serializer_class = BaseListSerializer

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        if not hasattr(instance, 'imdgamendment') or \
           not instance.imdgamendment or \
           not instance.imdgamendment.pages_directory_path:
            return representation

        pages_directory_path = instance.imdgamendment.pages_directory_path
        
        original_pdf_regions = representation.get('pdf_regions')

        if not isinstance(original_pdf_regions, list):
            return representation

        transformed_pdf_regions = []
        for region_data in original_pdf_regions:
            page_number = region_data.get('number_page') 
            coordinates = region_data.get('coordinates')

            if page_number is not None:
                media_url = settings.MEDIA_URL
                file_specific_path = f"{pages_directory_path}/{page_number}.pdf"
                link = f"{media_url}{file_specific_path}"
                
                transformed_pdf_regions.append({
                    'number_page': page_number,
                    'coordinates': coordinates,
                    'link_pdf': link
                    
                })
            else:
                transformed_pdf_regions.append(region_data) 
        
        representation['pdf_regions'] = transformed_pdf_regions
        return representation

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
                  'pdf_regions',
                  'description']
        list_serializer_class = BaseListSerializer

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        if not hasattr(instance, 'imdgamendment') or \
           not instance.imdgamendment or \
           not instance.imdgamendment.pages_directory_path:
            return representation

        pages_directory_path = instance.imdgamendment.pages_directory_path
        
        original_pdf_regions = representation.get('pdf_regions')

        if not isinstance(original_pdf_regions, list):
            return representation

        transformed_pdf_regions = []
        for region_data in original_pdf_regions:
            page_number = region_data.get('number_page') 
            coordinates = region_data.get('coordinates')

            if page_number is not None:
                media_url = settings.MEDIA_URL
                file_specific_path = f"{pages_directory_path}/{page_number}.pdf"
                link = f"{media_url}{file_specific_path}"
                
                transformed_pdf_regions.append({
                    'number_page': page_number,
                    'coordinates': coordinates,
                    'link_pdf': link
                    
                })
            else:
                transformed_pdf_regions.append(region_data) 
        
        representation['pdf_regions'] = transformed_pdf_regions
        return representation
        
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
                  'pdf_regions',
                  'description']
        list_serializer_class = BaseListSerializer

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        if not hasattr(instance, 'imdgamendment') or \
           not instance.imdgamendment or \
           not instance.imdgamendment.pages_directory_path:
            return representation

        pages_directory_path = instance.imdgamendment.pages_directory_path
        
        original_pdf_regions = representation.get('pdf_regions')

        if not isinstance(original_pdf_regions, list):
            return representation

        transformed_pdf_regions = []
        for region_data in original_pdf_regions:
            page_number = region_data.get('number_page') 
            coordinates = region_data.get('coordinates')

            if page_number is not None:
                media_url = settings.MEDIA_URL
                file_specific_path = f"{pages_directory_path}/{page_number}.pdf"
                link = f"{media_url}{file_specific_path}"
                
                transformed_pdf_regions.append({
                    'number_page': page_number,
                    'coordinates': coordinates,
                    'link_pdf': link
                    
                })
            else:
                transformed_pdf_regions.append(region_data) 
        
        representation['pdf_regions'] = transformed_pdf_regions
        return representation

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
                  'pdf_regions',
                  'description']
        list_serializer_class = BaseListSerializer
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        if not hasattr(instance, 'imdgamendment') or \
           not instance.imdgamendment or \
           not instance.imdgamendment.pages_directory_path:
            return representation

        pages_directory_path = instance.imdgamendment.pages_directory_path
        
        original_pdf_regions = representation.get('pdf_regions')

        if not isinstance(original_pdf_regions, list):
            return representation

        transformed_pdf_regions = []
        for region_data in original_pdf_regions:
            page_number = region_data.get('number_page') 
            coordinates = region_data.get('coordinates')

            if page_number is not None:
                media_url = settings.MEDIA_URL
                file_specific_path = f"{pages_directory_path}/{page_number}.pdf"
                link = f"{media_url}{file_specific_path}"
                
                transformed_pdf_regions.append({
                    'number_page': page_number,
                    'coordinates': coordinates,
                    'link_pdf': link
                    
                })
            else:
                transformed_pdf_regions.append(region_data) 
        
        representation['pdf_regions'] = transformed_pdf_regions
        return representation

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
                  'pdf_regions',
                  'description']
        list_serializer_class = BaseListSerializer
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        if not hasattr(instance, 'imdgamendment') or \
           not instance.imdgamendment or \
           not instance.imdgamendment.pages_directory_path:
            return representation

        pages_directory_path = instance.imdgamendment.pages_directory_path
        
        original_pdf_regions = representation.get('pdf_regions')

        if not isinstance(original_pdf_regions, list):
            return representation

        transformed_pdf_regions = []
        for region_data in original_pdf_regions:
            page_number = region_data.get('number_page') 
            coordinates = region_data.get('coordinates')

            if page_number is not None:
                media_url = settings.MEDIA_URL
                file_specific_path = f"{pages_directory_path}/{page_number}.pdf"
                link = f"{media_url}{file_specific_path}"
                
                transformed_pdf_regions.append({
                    'number_page': page_number,
                    'coordinates': coordinates,
                    'link_pdf': link
                    
                })
            else:
                transformed_pdf_regions.append(region_data) 
        
        representation['pdf_regions'] = transformed_pdf_regions
        return representation

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
                  'pdf_regions',
                  'description']
        list_serializer_class = BaseListSerializer

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        if not hasattr(instance, 'imdgamendment') or \
           not instance.imdgamendment or \
           not instance.imdgamendment.pages_directory_path:
            return representation

        pages_directory_path = instance.imdgamendment.pages_directory_path
        
        original_pdf_regions = representation.get('pdf_regions')

        if not isinstance(original_pdf_regions, list):
            return representation

        transformed_pdf_regions = []
        for region_data in original_pdf_regions:
            page_number = region_data.get('number_page') 
            coordinates = region_data.get('coordinates')

            if page_number is not None:
                media_url = settings.MEDIA_URL
                file_specific_path = f"{pages_directory_path}/{page_number}.pdf"
                link = f"{media_url}{file_specific_path}"
                
                transformed_pdf_regions.append({
                    'number_page': page_number,
                    'coordinates': coordinates,
                    'link_pdf': link
                    
                })
            else:
                transformed_pdf_regions.append(region_data) 
        
        representation['pdf_regions'] = transformed_pdf_regions
        return representation

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
                  'pdf_regions',
                  'description']
        list_serializer_class = BaseListSerializer
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        if not hasattr(instance, 'imdgamendment') or \
           not instance.imdgamendment or \
           not instance.imdgamendment.pages_directory_path:
            return representation

        pages_directory_path = instance.imdgamendment.pages_directory_path
        
        original_pdf_regions = representation.get('pdf_regions')

        if not isinstance(original_pdf_regions, list):
            return representation

        transformed_pdf_regions = []
        for region_data in original_pdf_regions:
            page_number = region_data.get('number_page') 
            coordinates = region_data.get('coordinates')

            if page_number is not None:
                media_url = settings.MEDIA_URL
                file_specific_path = f"{pages_directory_path}/{page_number}.pdf"
                link = f"{media_url}{file_specific_path}"
                
                transformed_pdf_regions.append({
                    'number_page': page_number,
                    'coordinates': coordinates,
                    'link_pdf': link
                    
                })
            else:
                transformed_pdf_regions.append(region_data) 
        
        representation['pdf_regions'] = transformed_pdf_regions
        return representation

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
                  'pdf_regions',
                  'description']
        list_serializer_class = BaseListSerializer
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        if not hasattr(instance, 'imdgamendment') or \
           not instance.imdgamendment or \
           not instance.imdgamendment.pages_directory_path:
            return representation

        pages_directory_path = instance.imdgamendment.pages_directory_path
        
        original_pdf_regions = representation.get('pdf_regions')

        if not isinstance(original_pdf_regions, list):
            return representation

        transformed_pdf_regions = []
        for region_data in original_pdf_regions:
            page_number = region_data.get('number_page') 
            coordinates = region_data.get('coordinates')

            if page_number is not None:
                media_url = settings.MEDIA_URL
                file_specific_path = f"{pages_directory_path}/{page_number}.pdf"
                link = f"{media_url}{file_specific_path}"
                
                transformed_pdf_regions.append({
                    'number_page': page_number,
                    'coordinates': coordinates,
                    'link_pdf': link
                    
                })
            else:
                transformed_pdf_regions.append(region_data) 
        
        representation['pdf_regions'] = transformed_pdf_regions
        return representation

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
                  'pdf_regions',
                  'description']
        list_serializer_class = BaseListSerializer

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        if not hasattr(instance, 'imdgamendment') or \
           not instance.imdgamendment or \
           not instance.imdgamendment.pages_directory_path:
            return representation

        pages_directory_path = instance.imdgamendment.pages_directory_path
        
        original_pdf_regions = representation.get('pdf_regions')

        if not isinstance(original_pdf_regions, list):
            return representation

        transformed_pdf_regions = []
        for region_data in original_pdf_regions:
            page_number = region_data.get('number_page') 
            coordinates = region_data.get('coordinates')

            if page_number is not None:
                media_url = settings.MEDIA_URL
                file_specific_path = f"{pages_directory_path}/{page_number}.pdf"
                link = f"{media_url}{file_specific_path}"
                
                transformed_pdf_regions.append({
                    'number_page': page_number,
                    'coordinates': coordinates,
                    'link_pdf': link
                    
                })
            else:
                transformed_pdf_regions.append(region_data) 
        
        representation['pdf_regions'] = transformed_pdf_regions
        return representation


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

