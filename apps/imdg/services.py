from .models import (
    IMDGAmendment, DangerousGoods, ClassDivision, SegregationRule
)

class IMDGLookupService:
    def __init__(self):
        try:
            self.active_amendment = IMDGAmendment.objects.get(is_effective=True)
        except IMDGAmendment.DoesNotExist:
            self.active_amendment = None
        except IMDGAmendment.MultipleObjectsReturned:
            self.active_amendment = IMDGAmendment.objects.filter(is_effective=True).latest('upload_at')

    def _find_related_object(self, model_class, code):
        if not code or not self.active_amendment: return None
        try:
            return model_class.objects.get(code=code, imdgamendment=self.active_amendment)
        except model_class.DoesNotExist:
            return None

    def _find_related_objects_from_list(self, model_class, code_list):
        if not code_list or not isinstance(code_list, list) or not self.active_amendment:
            return []
        return list(model_class.objects.filter(code__in=code_list, imdgamendment=self.active_amendment))

    def get_computed_details(self, dg_instance: DangerousGoods):
        if not self.active_amendment or not dg_instance: return {}

        primary_class = self._find_related_object(ClassDivision, dg_instance.class_division_code)
        subsidiary_hazards = self._find_related_objects_from_list(ClassDivision, dg_instance.subsidiary_hazards_codes or [])

        required_labels = []
        if primary_class and primary_class.label:
            required_labels.append(primary_class.label.url)
        for sub_risk in subsidiary_hazards:
            if sub_risk and sub_risk.label:
                required_labels.append(sub_risk.label.url)

        segregation_rules = []
        if primary_class:
            rules = SegregationRule.objects.filter(
                imdgamendment=self.active_amendment,
                fromclass=primary_class
            ).select_related('toclass')
            segregation_rules = [{'to_class_code': rule.toclass.code, 'requirement': rule.requirement} for rule in rules]

        return {
            'package_labels': required_labels,
            'ctu_placards': required_labels,
            'segregation_rules': segregation_rules
        }