from django.db import models

class UNCode(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=4, unique=True)
    description = models.JSONField(default=dict)
    is_activate = models.BooleanField(default=True)
    class Meta:
        db_table = 'goods.uncode'

class Classification(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=1, unique=True)
    label = models.ImageField(upload_to='labels/class/', null=True, blank=True)
    description = models.JSONField(default=dict)
    is_activate = models.BooleanField(default=True)
    class Meta:
        db_table = 'goods.classification'

class Division(models.Model):
    id = models.AutoField(primary_key=True)
    classification = models.ForeignKey(Classification, on_delete=models.CASCADE, related_name='divisions')
    code = models.CharField(max_length=1)
    label = models.ImageField(upload_to='labels/division/', null=True, blank=True)
    description = models.JSONField(default=dict)
    is_activate = models.BooleanField(default=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['classification', 'code'], name='unique_class_code'
            )
        ]
        db_table = 'goods.division'

class CompatibilityGroup(models.Model):
    id = models.AutoField(primary_key=True)
    classification = models.ForeignKey(Classification, on_delete=models.CASCADE, related_name='compatibility_groups')
    division = models.ForeignKey(Division, on_delete=models.CASCADE, related_name='compatibility_groups')
    code = models.CharField(max_length=1)
    description = models.JSONField(default=dict)
    is_activate = models.BooleanField(default=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['classification', 'division', 'code'], name='unique_class_division_code'
            )
        ]
        db_table = 'goods.compatibilitygroup'

class ClassDivisionGroup(models.Model):
    id = models.BigAutoField(primary_key=True)
    classification = models.ForeignKey(Classification, on_delete=models.CASCADE, related_name='class_divisions')
    division = models.ForeignKey(Division, on_delete=models.CASCADE, null=True, blank=True, related_name='class_divisions')
    compatibility_group = models.ForeignKey(CompatibilityGroup, on_delete=models.CASCADE, blank=True, null=True, related_name='class_divisions')
    is_activate = models.BooleanField(default=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['classification', 'division', 'compatibility_group'], name='unique_class_division_group'
            )
        ]
        db_table = 'goods.class_division_group'


class PackingGroup(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=1, unique=True)
    description = models.JSONField(default=dict)
    is_activate = models.BooleanField(default=True)
    class Meta:
        db_table = 'goods.packinggroup'

class SpecialProvisions(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=3, unique=True)
    description = models.JSONField(default=dict)
    is_activate = models.BooleanField(default=True)
    class Meta:
        db_table = 'goods.specialprovisions'

class ExceptedQuantities(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=2, unique=True)
    description = models.JSONField(default=dict)
    is_activate = models.BooleanField(default=True)
    class Meta:
        db_table = 'goods.exceptedquantities'

class PackingInstructions(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.JSONField(default=dict)
    is_activate = models.BooleanField(default=True)
    class Meta:
        db_table = 'goods.packinginstructions'

class PackingProvisions(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.JSONField(default=dict)
    is_activate = models.BooleanField(default=True)
    class Meta:
        db_table = 'goods.packingprovisions'

class IBCInstructions(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.JSONField(default=dict)
    is_activate = models.BooleanField(default=True)
    class Meta:
        db_table = 'goods.ibcinstructions'

class IBCProvisions(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.JSONField(default=dict)
    is_activate = models.BooleanField(default=True)
    class Meta:
        db_table = 'goods.ibcprovisions'

class TankInstructions(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.JSONField(default=dict)
    is_activate = models.BooleanField(default=True)
    class Meta:
        db_table = 'goods.tankinstructions'

class TankProvisions(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.JSONField(default=dict)
    is_activate = models.BooleanField(default=True)
    class Meta:
        db_table = 'goods.tankprovisions'

class EmergencySchedule(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.JSONField(default=dict)
    is_activate = models.BooleanField(default=True)
    class Meta:
        db_table = 'goods.emergencyschedule'

class StowageHandling(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=3, unique=True)
    description = models.JSONField(default=dict)
    is_activate = models.BooleanField(default=True)
    class Meta:
        db_table = 'goods.stowagehandling'

class Segregation(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.JSONField(default=dict)
    is_activate = models.BooleanField(default=True)
    class Meta:
        db_table = 'goods.segregation'

class DangerousGoods(models.Model):
    id = models.BigAutoField(primary_key=True)
    un_code = models.ForeignKey(UNCode, on_delete=models.CASCADE, related_name='dangerousgoods')
    proper_shipping_name = models.TextField(null=True, blank=True)
    class_division = models.ForeignKey(ClassDivisionGroup, on_delete=models.CASCADE, null=True, blank=True, related_name='dangerousgoods')
    subsidiary_hazards = models.ManyToManyField(ClassDivisionGroup, blank=True, related_name='dangerousgoods_subsidiaryhazards')
    packing_group = models.ForeignKey(PackingGroup, on_delete=models.CASCADE, null=True, blank=True, related_name='dangerousgoods')
    special_provisions = models.ManyToManyField(SpecialProvisions, blank=True, related_name='dangerousgoods_specialprovisions')
    limited_quantities = models.CharField(max_length=100, null=True, blank=True)
    excepted_quantities = models.ManyToManyField(ExceptedQuantities, blank=True, related_name='dangerousgoods_exceptedquantities')
    packing_instructions = models.ManyToManyField(PackingInstructions, blank=True, related_name='dangerousgoods_packinginstructions')
    packing_provisions = models.ManyToManyField(PackingProvisions, blank=True, related_name='dangerousgoods_packingprovisions')
    ibc_instructions = models.ManyToManyField(IBCInstructions, blank=True, related_name='dangerousgoods_ibcinstructions')
    ibc_provisions = models.ManyToManyField(IBCProvisions, blank=True, related_name='dangerousgoods_ibcprovisions')
    tank_instructions = models.ManyToManyField(TankInstructions, blank=True, related_name='dangerousgoods_tankinstructions')
    tank_provisions = models.ManyToManyField(TankProvisions, blank=True, related_name='dangerousgoods_tankprovisions')
    emergency_schedule = models.ManyToManyField(EmergencySchedule, blank=True, related_name='dangerousgoods_emergencyschedule')
    stowage_handling = models.ManyToManyField(StowageHandling, blank=True, related_name='dangerousgoods_stowagehandling')
    segregation = models.ManyToManyField(Segregation, blank=True, related_name='dangerousgoods_segregation')
    observations = models.TextField(null=True, blank=True)
    is_activate = models.BooleanField(default=True)
    class Meta:
        db_table = 'goods.dangerousgoods'

class SegregationBar(models.Model): 
    id = models.BigAutoField(primary_key=True)
    from_class = models.ForeignKey(ClassDivisionGroup, on_delete=models.CASCADE, related_name='from_class')
    to_class = models.ForeignKey(ClassDivisionGroup, on_delete=models.CASCADE, related_name='to_class')
    segregation_level = models.SmallIntegerField(default=0)
    is_activate = models.BooleanField(default=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['from_class', 'to_class'], name='unique_from_to_class'
            )
        ]
        db_table = 'goods.segregationbar'