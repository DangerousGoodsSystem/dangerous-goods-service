from django.db import models, transaction

class IMDGAmendment(models.Model):
    name = models.CharField(max_length=10, unique=True)
    is_effective = models.BooleanField(default=False)
    upload_at = models.DateTimeField(auto_now_add=True)
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
    description = models.JSONField(null=True, blank=True)
    upload_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['imdgamendment', 'code'], name='unique_imdgamendment_uncode'
            )
        ]
        ordering = ['-upload_at']
        db_table = 'imdg.uncode'
    
class ClassDivision(models.Model):
    id = models.AutoField(primary_key=True)
    imdgamendment = models.ForeignKey(IMDGAmendment, on_delete=models.CASCADE, related_name='classdivisions')
    code = models.CharField(max_length=10)
    label = models.ImageField(upload_to='pictures/imdg/classdivisions/', null=True, blank=True)
    description = models.JSONField(null=True, blank=True)
    upload_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['imdgamendment', 'code'], name='unique_imdgamendment_classdivisioncode'
            )
        ]
        ordering = ['-upload_at']
        db_table = 'imdg.classdivision'


class PackingGroup(models.Model):
    id = models.AutoField(primary_key=True)
    imdgamendment = models.ForeignKey(IMDGAmendment, on_delete=models.CASCADE, related_name='packing_groups')
    code = models.CharField(max_length=10)
    file = models.FileField(upload_to='documents/imdg/packinggroups/', null=True, blank=True)
    description = models.JSONField(null=True, blank=True)
    upload_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['imdgamendment', 'code'], name='unique_imdgamendment_packinggroupcode'
            )
        ]
        ordering = ['-upload_at']
        db_table = 'imdg.packinggroup'

class SpecialProvisions(models.Model):
    id = models.AutoField(primary_key=True)
    imdgamendment = models.ForeignKey(IMDGAmendment, on_delete=models.CASCADE, related_name='special_provisions')
    code = models.CharField(max_length=10)
    file = models.FileField(upload_to='documents/imdg/specialprovisions/', null=True, blank=True)
    description = models.JSONField(null=True, blank=True)
    upload_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['imdgamendment', 'code'], name='unique_imdgamendment_specialprovisioncode'
            )
        ]
        ordering = ['-upload_at']
        db_table = 'imdg.specialprovisions'

class ExceptedQuantities(models.Model):
    id = models.AutoField(primary_key=True)
    imdgamendment = models.ForeignKey(IMDGAmendment, on_delete=models.CASCADE, related_name='excepted_quantities')
    code = models.CharField(max_length=10)
    file = models.FileField(upload_to='documents/imdg/exceptedquantities/', null=True, blank=True)
    description = models.JSONField(null=True, blank=True)
    upload_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['imdgamendment', 'code'], name='unique_imdgamendment_exceptedquantitiecode'
            )
        ]
        ordering = ['-upload_at']
        db_table = 'imdg.exceptedquantities'

class PackingInstructions(models.Model):
    id = models.AutoField(primary_key=True)
    imdgamendment = models.ForeignKey(IMDGAmendment, on_delete=models.CASCADE, related_name='packing_instructions')
    code = models.CharField(max_length=10)
    file = models.FileField(upload_to='documents/imdg/packinginstructions/', null=True, blank=True)
    description = models.JSONField(null=True, blank=True)
    upload_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['imdgamendment', 'code'], name='unique_imdgamendment_packinginstructioncode'
            )
        ]
        ordering = ['-upload_at']
        db_table = 'imdg.packinginstructions'

class PackingProvisions(models.Model):
    id = models.AutoField(primary_key=True)
    imdgamendment = models.ForeignKey(IMDGAmendment, on_delete=models.CASCADE, related_name='packing_provisions')
    code = models.CharField(max_length=10)
    file = models.FileField(upload_to='documents/imdg/packingprovisions/', null=True, blank=True)
    description = models.JSONField(null=True, blank=True)
    upload_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['imdgamendment', 'code'], name='unique_imdgamendment_packingprovisioncode'
            )
        ]
        ordering = ['-upload_at']
        db_table = 'imdg.packingprovisions'

class IBCInstructions(models.Model):
    id = models.AutoField(primary_key=True)
    imdgamendment = models.ForeignKey(IMDGAmendment, on_delete=models.CASCADE, related_name='ibc_instructions')
    code = models.CharField(max_length=10)
    file = models.FileField(upload_to='documents/imdg/ibcinstructions/', null=True, blank=True)
    description = models.JSONField(null=True, blank=True)
    upload_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['imdgamendment', 'code'], name='unique_imdgamendment_ibcinstructioncode'
            )
        ]
        ordering = ['-upload_at']
        db_table = 'imdg.ibcinstructions'

class IBCProvisions(models.Model):
    id = models.AutoField(primary_key=True)
    imdgamendment = models.ForeignKey(IMDGAmendment, on_delete=models.CASCADE, related_name='ibc_provisions')
    code = models.CharField(max_length=10)
    file = models.FileField(upload_to='documents/imdg/ibcprovisions/', null=True, blank=True)
    description = models.JSONField(null=True, blank=True)
    upload_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['imdgamendment', 'code'], name='unique_imdgamendment_ibcprovisioncode'
            )
        ]
        ordering = ['-upload_at']
        db_table = 'imdg.ibcprovisions'

class TankInstructions(models.Model):
    id = models.AutoField(primary_key=True)
    imdgamendment = models.ForeignKey(IMDGAmendment, on_delete=models.CASCADE, related_name='tank_instructions')
    code = models.CharField(max_length=10)
    file = models.FileField(upload_to='documents/imdg/tankinstructions/', null=True, blank=True)
    description = models.JSONField(null=True, blank=True)
    upload_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['imdgamendment', 'code'], name='unique_imdgamendment_tankinstructioncode'
            )
        ]
        ordering = ['-upload_at']
        db_table = 'imdg.tankinstructions'

class TankProvisions(models.Model):
    id = models.AutoField(primary_key=True)
    imdgamendment = models.ForeignKey(IMDGAmendment, on_delete=models.CASCADE, related_name='tank_provisions')
    code = models.CharField(max_length=10)
    file = models.FileField(upload_to='documents/imdg/tankprovisions/', null=True, blank=True)
    description = models.JSONField(null=True, blank=True)
    upload_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['imdgamendment', 'code'], name='unique_imdgamendment_tankprovisioncode'
            )
        ]
        ordering = ['-upload_at']
        db_table = 'imdg.tankprovisions'

class EmergencySchedules(models.Model):
    id = models.AutoField(primary_key=True)
    imdgamendment = models.ForeignKey(IMDGAmendment, on_delete=models.CASCADE, related_name='emergency_schedules')
    code = models.CharField(max_length=10)
    file = models.FileField(upload_to='documents/imdg/emergencyschedules/', null=True, blank=True)
    description = models.JSONField(null=True, blank=True)
    upload_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['imdgamendment', 'code'], name='unique_imdgamendment_emergencyschedulecode'
            )
        ]
        ordering = ['-upload_at']
        db_table = 'imdg.emergencyschedules'

class StowageHandling(models.Model):
    id = models.AutoField(primary_key=True)
    imdgamendment = models.ForeignKey(IMDGAmendment, on_delete=models.CASCADE, related_name='stowage_handlings')
    code = models.CharField(max_length=10)
    file = models.FileField(upload_to='documents/imdg/stowagehandling/', null=True, blank=True)
    description = models.JSONField(null=True, blank=True)
    upload_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['imdgamendment', 'code'], name='unique_imdgamendment_stowagehandlingcode'
            )
        ]
        ordering = ['-upload_at']
        db_table = 'imdg.stowagehandling'

class Segregation(models.Model):
    id = models.AutoField(primary_key=True)
    imdgamendment = models.ForeignKey(IMDGAmendment, on_delete=models.CASCADE, related_name='segregations')
    code = models.CharField(max_length=10)
    file = models.FileField(upload_to='documents/imdg/segregations/', null=True, blank=True)
    description = models.JSONField(null=True, blank=True)
    upload_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['imdgamendment', 'code'], name='unique_imdgamendment_segregationcode'
            )
        ]
        ordering = ['-upload_at']
        db_table = 'imdg.segregation'

class SegregationRule(models.Model):
    SEGREGATION_REQUIREMENT_CHOICES = [
        ('1', '1 - Away from'),
        ('2', '2 - Separated from'),
        ('3', '3 - Separated by a complete compartment or hold from'),
        ('4', '4 - Separated longitudinally by an intervening complete compartment or hold from'),
        ('X', 'X - No general segregation provisions apply. Check DGL.'),
        ('*', '* - See compatibility group requirements for explosives.'),
    ]
    id = models.AutoField(primary_key=True)
    imdgamendment = models.ForeignKey(IMDGAmendment, on_delete=models.CASCADE, related_name='segregation_bars')
    fromclass = models.ForeignKey(ClassDivision, on_delete=models.CASCADE, related_name='from_class')
    toclass = models.ForeignKey(ClassDivision, on_delete=models.CASCADE, related_name='to_class')
    requirement = models.CharField(max_length=1, choices=SEGREGATION_REQUIREMENT_CHOICES, default='X')
    upload_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['imdgamendment', 'fromclass', 'toclass'], name='unique_imdgamendment_segregationbar'
            )
        ]
        ordering = ['-upload_at']
        db_table = 'imdg.segregationrule'


class DangerousGoods(models.Model):
    id = models.BigAutoField(primary_key=True)
    imdgamendment = models.ForeignKey(IMDGAmendment, on_delete=models.CASCADE, related_name='dangerousgoods')
    un_code = models.CharField(max_length=4, null=True, blank=True)
    proper_shipping_name = models.TextField(null=True, blank=True)
    class_division_code = models.CharField(max_length=10, null=True, blank=True)
    subsidiary_hazards_codes = models.JSONField(null=True, blank=True)
    packing_group_code = models.CharField(max_length=10, null=True, blank=True)
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
    upload_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-upload_at']
        db_table = 'imdg.dangerousgoods'