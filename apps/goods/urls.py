from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UNCodeViewSet, UNCodeImageViewSet,
    ClassificationViewSet,
    DivisionViewSet,
    CompatibilityGroupViewSet,
    PackingGroupViewSet, PackingGroupImageViewSet,
    SpecialProvisionsViewSet, SpecialProvisionsImageViewSet,
    ExceptedQuantitiesViewSet, ExceptedQuantitiesImageViewSet,
    PackingInstructionsViewSet, PackingInstructionsImageViewSet,
    PackingProvisionsViewSet, PackingProvisionsImageViewSet,
    IBCInstructionsViewSet, IBCInstructionsImageViewSet,
    IBCProvisionsViewSet, IBCProvisionsImageViewSet,
    TankInstructionsViewSet, TankInstructionsImageViewSet,
    TankProvisionsViewSet, TankProvisionsImageViewSet,
    EmergencyScheduleViewSet, EmergencyScheduleImageViewSet,
    StowageHandlingViewSet, StowageHandlingImageViewSet,
    SegregationViewSet, SegregationImageViewSet,
    SegregationBarViewSet,
    DangerousGoodsViewSet,
    SearchDangerousGoodsViewSet,
    )

router = DefaultRouter()
router.register(r'un-codes', UNCodeViewSet, basename='un_codes')
router.register(r'classifications', ClassificationViewSet, basename='classifications')
router.register(r'divisions', DivisionViewSet, basename='divisions')    
router.register(r'compatibility-groups', CompatibilityGroupViewSet, basename='compatibility_groups')
router.register(r'packing-groups', PackingGroupViewSet, basename='packing_groups')
router.register(r'special-provisions', SpecialProvisionsViewSet, basename='special_provisions')
router.register(r'excepted-quantities', ExceptedQuantitiesViewSet, basename='excepted_quantities')
router.register(r'packing-instructions', PackingInstructionsViewSet, basename='packing_instructions')
router.register(r'packing-provisions', PackingProvisionsViewSet, basename='packing_provisions')
router.register(r'ibc-instructions', IBCInstructionsViewSet, basename='ibc_instructions')
router.register(r'ibc-provisions', IBCProvisionsViewSet, basename='ibc_provisions')
router.register(r'tank-instructions', TankInstructionsViewSet, basename='tank_instructions')
router.register(r'tank-provisions', TankProvisionsViewSet, basename='tank_provisions')
router.register(r'emergency-schedules', EmergencyScheduleViewSet, basename='emergency_schedules')
router.register(r'stowage-handling', StowageHandlingViewSet, basename='stowage_handling')
router.register(r'segregations', SegregationViewSet, basename='segregations')
router.register(r'dangerous-goods', DangerousGoodsViewSet, basename='dangerous_goods')
router.register(r'segregation-bars', SegregationBarViewSet, basename='segregation_bars')
router.register(r'search-dangerous-goods', SearchDangerousGoodsViewSet, basename='search-dangerous-goods')

# Image viewsets
router.register(r'un-codes-images', UNCodeImageViewSet, basename='un_codes_images')
router.register(r'packing-groups-images', PackingGroupImageViewSet, basename='packing_groups_images')
router.register(r'special-provisions-images', SpecialProvisionsImageViewSet, basename='special_provisions_images')
router.register(r'excepted-quantities-images', ExceptedQuantitiesImageViewSet, basename='excepted_quantities_images')
router.register(r'packing-instructions-images', PackingInstructionsImageViewSet, basename='packing_instructions_images')
router.register(r'packing-provisions-images', PackingProvisionsImageViewSet, basename='packing_provisions_images')
router.register(r'ibc-instructions-images', IBCInstructionsImageViewSet, basename='ibc_instructions_images')
router.register(r'ibc-provisions-images', IBCProvisionsImageViewSet, basename='ibc_provisions_images')
router.register(r'tank-instructions-images', TankInstructionsImageViewSet, basename='tank_instructions_images')
router.register(r'tank-provisions-images', TankProvisionsImageViewSet, basename='tank_provisions_images')
router.register(r'emergency-schedules-images', EmergencyScheduleImageViewSet, basename='emergency_schedules_images')
router.register(r'stowage-handling-images', StowageHandlingImageViewSet, basename='stowage_handling_images')
router.register(r'segregations-images', SegregationImageViewSet, basename='segregations_images')

urlpatterns = [
    path('', include(router.urls)),
]