from django.db import models, transaction

class IMDGAmendment(models.Model):
    file = models.FileField(upload_to='documents/imdg/amendments/')
    pages_directory_path = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=10, unique=True)
    upload_at = models.DateTimeField(auto_now_add=True)
    is_effective = models.BooleanField(default=False)
    class Meta:
        ordering = ['-upload_at']
        db_table = 'imdg.imdgamendment'

    def save(self, *args, **kwargs):
        if self.is_effective:
            with transaction.atomic():
                qs = IMDGAmendment.objects.filter(is_effective=True)
                if self.pk:
                    qs = qs.exclude(pk=self.pk)
                qs.update(is_effective=False)
        super().save(*args, **kwargs)

class UNCode(models.Model):
    id = models.AutoField(primary_key=True)
    imdgamendment = models.ForeignKey(IMDGAmendment, on_delete=models.CASCADE, related_name='uncodes')
    code = models.CharField(max_length=4)
    description = models.TextField(null=True, blank=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['imdgamendment', 'code'], name='unique_imdgamendment_uncode'
            )
        ]
        db_table = 'imdg.uncode'
    
class Classification(models.Model):
    id = models.AutoField(primary_key=True)
    imdgamendment = models.ForeignKey(IMDGAmendment, on_delete=models.CASCADE, related_name='classifications')
    code = models.CharField(max_length=1)
    label = models.ImageField(upload_to='labels/class/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['imdgamendment', 'code'], name='unique_imdgamendment_classificationcode'
            )
        ]
        db_table = 'imdg.classification'

class Division(models.Model):
    id = models.AutoField(primary_key=True)
    imdgamendment = models.ForeignKey(IMDGAmendment, on_delete=models.CASCADE, related_name='divisions')
    classification = models.ForeignKey(Classification, on_delete=models.CASCADE, related_name='divisions')
    code = models.CharField(max_length=1)
    label = models.ImageField(upload_to='labels/division/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['imdgamendment', 'classification', 'code'], name='unique_imdgamendment_classification_divisioncode'
            )
        ]
        db_table = 'imdg.division'

class CompatibilityGroup(models.Model):
    id = models.AutoField(primary_key=True)
    imdgamendment = models.ForeignKey(IMDGAmendment, on_delete=models.CASCADE, related_name='compatibility_groups')
    division = models.ForeignKey(Division, on_delete=models.CASCADE, related_name='compatibility_groups')
    code = models.CharField(max_length=1)
    description = models.TextField(null=True, blank=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['imdgamendment', 'division', 'code'], name='unique_imdgamendment_division_compatibilitygroupcode'
            )
        ]
        db_table = 'imdg.compatibilitygroup'

class PackingGroup(models.Model):
    id = models.AutoField(primary_key=True)
    imdgamendment = models.ForeignKey(IMDGAmendment, on_delete=models.CASCADE, related_name='packing_groups')
    code = models.CharField(max_length=10)
    pdf_regions = models.JSONField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['imdgamendment', 'code'], name='unique_imdgamendment_packinggroupcode'
            )
        ]
        db_table = 'imdg.packinggroup'

class SpecialProvisions(models.Model):
    id = models.AutoField(primary_key=True)
    imdgamendment = models.ForeignKey(IMDGAmendment, on_delete=models.CASCADE, related_name='special_provisions')
    code = models.CharField(max_length=10)
    pdf_regions = models.JSONField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['imdgamendment', 'code'], name='unique_imdgamendment_specialprovisioncode'
            )
        ]
        db_table = 'imdg.specialprovisions'

class ExceptedQuantities(models.Model):
    id = models.AutoField(primary_key=True)
    imdgamendment = models.ForeignKey(IMDGAmendment, on_delete=models.CASCADE, related_name='excepted_quantities')
    code = models.CharField(max_length=10)
    pdf_regions = models.JSONField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['imdgamendment', 'code'], name='unique_imdgamendment_exceptedquantitiecode'
            )
        ]
        db_table = 'imdg.exceptedquantities'

class PackingInstructions(models.Model):
    id = models.AutoField(primary_key=True)
    imdgamendment = models.ForeignKey(IMDGAmendment, on_delete=models.CASCADE, related_name='packing_instructions')
    code = models.CharField(max_length=10)
    pdf_regions = models.JSONField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['imdgamendment', 'code'], name='unique_imdgamendment_packinginstructioncode'
            )
        ]
        db_table = 'imdg.packinginstructions'

class PackingProvisions(models.Model):
    id = models.AutoField(primary_key=True)
    imdgamendment = models.ForeignKey(IMDGAmendment, on_delete=models.CASCADE, related_name='packing_provisions')
    code = models.CharField(max_length=10)
    pdf_regions = models.JSONField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['imdgamendment', 'code'], name='unique_imdgamendment_packingprovisioncode'
            )
        ]
        db_table = 'imdg.packingprovisions'

class IBCInstructions(models.Model):
    id = models.AutoField(primary_key=True)
    imdgamendment = models.ForeignKey(IMDGAmendment, on_delete=models.CASCADE, related_name='ibc_instructions')
    code = models.CharField(max_length=10)
    pdf_regions = models.JSONField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['imdgamendment', 'code'], name='unique_imdgamendment_ibcinstructioncode'
            )
        ]
        db_table = 'imdg.ibcinstructions'

class IBCProvisions(models.Model):
    id = models.AutoField(primary_key=True)
    imdgamendment = models.ForeignKey(IMDGAmendment, on_delete=models.CASCADE, related_name='ibc_provisions')
    code = models.CharField(max_length=10)
    pdf_regions = models.JSONField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['imdgamendment', 'code'], name='unique_imdgamendment_ibcprovisioncode'
            )
        ]
        db_table = 'imdg.ibcprovisions'

class TankInstructions(models.Model):
    id = models.AutoField(primary_key=True)
    imdgamendment = models.ForeignKey(IMDGAmendment, on_delete=models.CASCADE, related_name='tank_instructions')
    code = models.CharField(max_length=10)
    pdf_regions = models.JSONField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['imdgamendment', 'code'], name='unique_imdgamendment_tankinstructioncode'
            )
        ]
        db_table = 'imdg.tankinstructions'

class TankProvisions(models.Model):
    id = models.AutoField(primary_key=True)
    imdgamendment = models.ForeignKey(IMDGAmendment, on_delete=models.CASCADE, related_name='tank_provisions')
    code = models.CharField(max_length=10)
    pdf_regions = models.JSONField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['imdgamendment', 'code'], name='unique_imdgamendment_tankprovisioncode'
            )
        ]
        db_table = 'imdg.tankprovisions'

class EmergencySchedules(models.Model):
    id = models.AutoField(primary_key=True)
    imdgamendment = models.ForeignKey(IMDGAmendment, on_delete=models.CASCADE, related_name='emergency_schedules')
    code = models.CharField(max_length=10)
    pdf_regions = models.JSONField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['imdgamendment', 'code'], name='unique_imdgamendment_emergencyschedulecode'
            )
        ]
        db_table = 'imdg.emergencyschedules'

class StowageHandling(models.Model):
    id = models.AutoField(primary_key=True)
    imdgamendment = models.ForeignKey(IMDGAmendment, on_delete=models.CASCADE, related_name='stowage_handlings')
    code = models.CharField(max_length=10)
    pdf_regions = models.JSONField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['imdgamendment', 'code'], name='unique_imdgamendment_stowagehandlingcode'
            )
        ]
        db_table = 'imdg.stowagehandling'

class Segregation(models.Model):
    id = models.AutoField(primary_key=True)
    imdgamendment = models.ForeignKey(IMDGAmendment, on_delete=models.CASCADE, related_name='segregations')
    code = models.CharField(max_length=10)
    pdf_regions = models.JSONField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['imdgamendment', 'code'], name='unique_imdgamendment_segregationcode'
            )
        ]
        db_table = 'imdg.segregation'


class DangerousGoods(models.Model):
    id = models.BigAutoField(primary_key=True)
    imdgamendment = models.ForeignKey(IMDGAmendment, on_delete=models.CASCADE, related_name='dangerousgoods')
    un_code = models.CharField(max_length=4)
    proper_shipping_name = models.TextField(null=True, blank=True)
    class_division_code = models.CharField(max_length=4, null=True, blank=True)
    subsidiary_hazards_codes = models.JSONField(null=True, blank=True)
    packing_group_code = models.CharField(max_length=3, null=True, blank=True)
    special_provisions_codes = models.JSONField(null=True, blank=True)
    limited_quantities = models.TextField(null=True, blank=True)
    excepted_quantities_codes = models.JSONField(null=True, blank=True)
    packing_instructions_codes = models.JSONField(null=True, blank=True)
    packing_provisions_codes = models.JSONField(null=True, blank=True)
    ibc_instructions_codes = models.JSONField(null=True, blank=True)
    ibc_provisions_codes = models.JSONField(null=True, blank=True)
    tank_instructions_codes = models.JSONField(null=True, blank=True)
    tank_provisions_codes =models.JSONField(null=True, blank=True)
    emergency_schedules_codes = models.JSONField(null=True, blank=True)
    stowage_handling_codes = models.JSONField(null=True, blank=True)
    segregation_codes = models.JSONField(null=True, blank=True)
    observations = models.TextField(null=True, blank=True)
    class Meta:
        db_table = 'imdg.dangerousgoods'