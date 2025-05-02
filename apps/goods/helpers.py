import re
from .models import Classification, Division, CompatibilityGroup, ClassDivisionGroup

def get_or_create_class_division_group(code_str):
    match = re.match(r'^([1-9])(?:\.(\d))?([A-Z])?$', code_str)
    if not match:
        raise ValueError("The value must be a string, for example '2', '2.1' or '1.1A'.")

    class_code, div_code, comp_code = match.groups()

    cls, _ = Classification.objects.get_or_create(
        code=class_code,
        defaults={'description': {}, 'activate': True}
    )

    div = None
    if div_code is not None:
        div, _ = Division.objects.get_or_create(
            classification=cls,
            code=div_code,
            defaults={'description': {}, 'activate': True}
        )

    comp = None
    if comp_code is not None:
        comp, _ = CompatibilityGroup.objects.get_or_create(
            classification=cls,
            division=div,
            code=comp_code,
            defaults={'description': {}, 'activate': True}
        )

    group, created = ClassDivisionGroup.objects.get_or_create(
        classification=cls,
        division=div,
        compatibility_group=comp,
        defaults={'activate': True}
    )

    return group, created

