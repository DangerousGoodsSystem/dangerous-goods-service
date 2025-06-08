
from .models import (
    IMDGAmendment, DangerousGoods, ClassDivision, SegregationRule, Segregation
)


class IMDGLookupService:
    """
    Lớp dịch vụ hoàn thiện, xử lý định dạng JSON và cung cấp đầy đủ
    thông tin về nhãn, biển báo, và các quy tắc phân cách.
    """
    def __init__(self):
        try:
            self.active_amendment = IMDGAmendment.objects.get(is_effective=True)
        except IMDGAmendment.DoesNotExist:
            print("Lỗi: Không có bộ luật IMDG nào được kích hoạt.")
            self.active_amendment = None
        except IMDGAmendment.MultipleObjectsReturned:
            print("Lỗi: Có nhiều hơn 1 bộ luật IMDG được kích hoạt.")
            self.active_amendment = IMDGAmendment.objects.filter(is_effective=True).latest('upload_at')

    def _find_related_object(self, model_class, code):
        if not code or not self.active_amendment: return None
        try:
            return model_class.objects.get(code=code, imdgamendment=self.active_amendment)
        except model_class.DoesNotExist:
            print(f"Không tìm thấy mã '{code}' trong {model_class.__name__} của {self.active_amendment.name}.")
            return None

    def _find_related_objects_from_list(self, model_class, code_list):
        if not code_list or not isinstance(code_list, list) or not self.active_amendment:
            return []
        return list(model_class.objects.filter(code__in=code_list, imdgamendment=self.active_amendment))

    def _get_required_labels(self, primary_class, subsidiary_hazards):
        label_urls = []
        if primary_class and primary_class.label:
            label_urls.append(primary_class.label.url)
        for sub_risk in subsidiary_hazards:
            if sub_risk and sub_risk.label:
                label_urls.append(sub_risk.label.url)
        return label_urls

    def _get_general_segregation_rules(self, primary_class):
        """Lấy quy tắc từ Bảng Phân cách chung (Segregation Table)."""
        if not primary_class: return []

        rules = SegregationRule.objects.filter(
            imdgamendment=self.active_amendment,
            fromclass=primary_class
        ).select_related('toclass')
        
        return [{
            'to_class_code': rule.toclass.code,
            'requirement': rule.requirement
        } for rule in rules]

    def _get_specific_segregation_details(self, segregation_codes):
        """Lấy mô tả cho các mã Segregation Code cụ thể (Cột 16b)."""
        if not segregation_codes: return []
        segregation_objects = self._find_related_objects_from_list(Segregation, segregation_codes)
        return [{
            'code': seg.code,
            'description': seg.description
        } for seg in segregation_objects]

    def get_computed_details(self, dg_instance: DangerousGoods, is_lq=False, is_eq=False):
        if not self.active_amendment or not dg_instance: return {}

        result = {'notes': []}
        
        # --- XỬ LÝ NGOẠI LỆ ---
        if is_eq:
            eq_codes = dg_instance.excepted_quantities_codes
            # Xử lý an toàn: kiểm tra xem có phải list và có phần tử không
            eq_code = eq_codes[0] if eq_codes and isinstance(eq_codes, list) and len(eq_codes) > 0 else None
            
            if eq_code and eq_code != 'E0':
                result.update({
                    'package_marks': [f"Dấu hiệu Excepted Quantities ({eq_code})"],
                    'package_labels': [], 'ctu_placards': []
                })
                result['notes'].append("Hàng EQ: Không yêu cầu nhãn và biển báo nguy hiểm.")
                return result
            else:
                result['notes'].append("Chất này không được phép vận chuyển dưới dạng Excepted Quantities.")
                return result

        if is_lq:
            if dg_instance.limited_quantities and dg_instance.limited_quantities != '0':
                result.update({
                    'package_marks': ["Dấu hiệu Limited Quantities (LQ)"],
                    'package_labels': [], 'ctu_placards': []
                })
                result['notes'].append("Hàng LQ: Không yêu cầu nhãn và biển báo nguy hiểm.")
                return result
            else:
                result['notes'].append("Chất này không được phép vận chuyển dưới dạng Limited Quantities.")
                return result
        
        primary_class = self._find_related_object(ClassDivision, dg_instance.class_division_code)
        subsidiary_hazards = self._find_related_objects_from_list(ClassDivision, dg_instance.subsidiary_hazards_codes or [])
        
        required_labels = self._get_required_labels(primary_class, subsidiary_hazards)
        general_seg_rules = self._get_general_segregation_rules(primary_class)
        specific_seg_details = self._get_specific_segregation_details(dg_instance.segregation_codes or [])

        result.update({
            'package_labels': required_labels,
            'ctu_placards': required_labels,
            'general_segregation_rules': general_seg_rules,
            'specific_segregation_details': specific_seg_details,
        })

        return result