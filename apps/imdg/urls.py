from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    IMDGAmendmentViewSet,
    UNCodeViewSet,
    ClassDivisionViewSet,
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
    SegregationRuleViewSet,
    DangerousGoodsViewSet,
    SearchDangerousGoodsViewSet,
    )

router = DefaultRouter()
router.register(r'imdg-amendments', IMDGAmendmentViewSet, basename='imdga_amendments')
router.register(r'un-codes', UNCodeViewSet, basename='un_codes')
router.register(r'class-divisions', ClassDivisionViewSet, basename='class_divisions')
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
router.register(r'segregation-rules', SegregationRuleViewSet, basename='segregation_rules')
router.register(r'search-dangerous-goods', SearchDangerousGoodsViewSet, basename='search-dangerous-goods')

urlpatterns = [
    path('', include(router.urls)),
]