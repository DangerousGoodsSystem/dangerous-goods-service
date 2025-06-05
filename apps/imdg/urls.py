from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    IMDGAmendmentViewSet,
    UNCodeViewSet,
    ClassificationViewSet,
    DivisionViewSet,
    CompatibilityGroupViewSet,
    PackingGroupViewSet,
    SpecialProvisionsViewSet,
    ExceptedQuantitiesViewSet,
    PackingInstructionsViewSet,
    PackingProvisionsViewSet,
    IBCInstructionsViewSet,
    IBCProvisionsViewSet,
    TankInstructionsViewSet,
    TankProvisionsViewSet,
    EmergencySchedulesViewSet,
    StowageHandlingViewSet,
    SegregationViewSet,
    DangerousGoodsViewSet,
    SearchDangerousGoodsViewSet,
    )

router = DefaultRouter()
router.register(r'imdg-amendments', IMDGAmendmentViewSet, basename='imdga_amendments')
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
router.register(r'emergency-schedules', EmergencySchedulesViewSet, basename='emergency_schedules')
router.register(r'stowage-handling', StowageHandlingViewSet, basename='stowage_handling')
router.register(r'segregations', SegregationViewSet, basename='segregations')
router.register(r'dangerous-goods', DangerousGoodsViewSet, basename='dangerous_goods')
router.register(r'search-dangerous-goods', SearchDangerousGoodsViewSet, basename='search-dangerous-goods')

urlpatterns = [
    path('', include(router.urls)),
]