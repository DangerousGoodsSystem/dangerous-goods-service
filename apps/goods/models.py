from django.db import models

class UNCode(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=4, unique=True)
    description = models.JSONField(default=dict)
    activate = models.BooleanField(default=True)
    class Meta:
        db_table = 'goods.uncode'

class Classification(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=1, unique=True)
    label = models.ImageField(upload_to='labels/class/', null=True, blank=True)
    description = models.JSONField(default=dict)
    activate = models.BooleanField(default=True)
    class Meta:
        db_table = 'goods.classification'

class Division(models.Model):
    id = models.AutoField(primary_key=True)
    classification = models.ForeignKey(Classification, on_delete=models.CASCADE, related_name='divisions')
    code = models.CharField(max_length=1)
    label = models.ImageField(upload_to='labels/division/', null=True, blank=True)
    description = models.JSONField(default=dict)
    activate = models.BooleanField(default=True)
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
    activate = models.BooleanField(default=True)
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
    activate = models.BooleanField(default=True)
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
    activate = models.BooleanField(default=True)
    class Meta:
        db_table = 'goods.packinggroup'

class SpecialProvisions(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=3, unique=True)
    description = models.JSONField(default=dict)
    activate = models.BooleanField(default=True)
    class Meta:
        db_table = 'goods.specialprovisions'

class ExceptedQuantities(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=2, unique=True)
    description = models.JSONField(default=dict)
    activate = models.BooleanField(default=True)
    class Meta:
        db_table = 'goods.exceptedquantities'

class PackingInstructions(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.JSONField(default=dict)
    activate = models.BooleanField(default=True)
    class Meta:
        db_table = 'goods.packinginstructions'

class PackingProvisions(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.JSONField(default=dict)
    activate = models.BooleanField(default=True)
    class Meta:
        db_table = 'goods.packingprovisions'

class IBCInstructions(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.JSONField(default=dict)
    activate = models.BooleanField(default=True)
    class Meta:
        db_table = 'goods.ibcinstructions'

class IBCProvisions(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.JSONField(default=dict)
    activate = models.BooleanField(default=True)
    class Meta:
        db_table = 'goods.ibcprovisions'

class TankInstructions(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.JSONField(default=dict)
    activate = models.BooleanField(default=True)
    class Meta:
        db_table = 'goods.tankinstructions'

class TankProvisions(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.JSONField(default=dict)
    activate = models.BooleanField(default=True)
    class Meta:
        db_table = 'goods.tankprovisions'

class EmergencySchedule(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.JSONField(default=dict)
    activate = models.BooleanField(default=True)
    class Meta:
        db_table = 'goods.emergencyschedule'

class StowageHandling(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=3, unique=True)
    description = models.JSONField(default=dict)
    activate = models.BooleanField(default=True)
    class Meta:
        db_table = 'goods.stowagehandling'

class Segregation(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.JSONField(default=dict)
    activate = models.BooleanField(default=True)
    class Meta:
        db_table = 'goods.segregation'

class DangerousGoods(models.Model):
    id = models.BigAutoField(primary_key=True)
    uncode = models.ForeignKey(UNCode, on_delete=models.CASCADE, related_name='dangerousgoods')
    propershippingname = models.TextField(null=True, blank=True)
    classdivision = models.ForeignKey(ClassDivisionGroup, on_delete=models.CASCADE, null=True, blank=True, related_name='dangerousgoods')
    subsidiaryhazards = models.ManyToManyField(ClassDivisionGroup, blank=True, related_name='dangerousgoods_subsidiaryhazards')
    packinggroup = models.ForeignKey(PackingGroup, on_delete=models.CASCADE, null=True, blank=True, related_name='dangerousgoods')
    specialprovisions = models.ManyToManyField(SpecialProvisions, blank=True, related_name='dangerousgoods_specialprovisions')
    limitedquantities = models.CharField(max_length=100, null=True, blank=True)
    exceptedquantities = models.ManyToManyField(ExceptedQuantities, blank=True, related_name='dangerousgoods_exceptedquantities')
    packinginstructions = models.ManyToManyField(PackingInstructions, blank=True, related_name='dangerousgoods_packinginstructions')
    packingprovisions = models.ManyToManyField(PackingProvisions, blank=True, related_name='dangerousgoods_packingprovisions')
    ibcinstructions = models.ManyToManyField(IBCInstructions, blank=True, related_name='dangerousgoods_ibcinstructions')
    ibcprovisions = models.ManyToManyField(IBCProvisions, blank=True, related_name='dangerousgoods_ibcprovisions')
    tankinstructions = models.ManyToManyField(TankInstructions, blank=True, related_name='dangerousgoods_tankinstructions')
    tankprovisions = models.ManyToManyField(TankProvisions, blank=True, related_name='dangerousgoods_tankprovisions')
    emergencyschedule = models.ManyToManyField(EmergencySchedule, blank=True, related_name='dangerousgoods_emergencyschedule')
    stowagehandling = models.ManyToManyField(StowageHandling, blank=True, related_name='dangerousgoods_stowagehandling')
    segregation = models.ManyToManyField(Segregation, blank=True, related_name='dangerousgoods_segregation')
    observations = models.TextField(null=True, blank=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['uncode', 'classdivision', 'packinggroup'], name='unique_un_division_packing'
            )
        ]
        db_table = 'goods.dangerousgoods'

class SegregationBar(models.Model): 
    id = models.BigAutoField(primary_key=True)
    fromclass = models.ForeignKey(ClassDivisionGroup, on_delete=models.CASCADE, related_name='segregationbars_from')
    toclass = models.ForeignKey(ClassDivisionGroup, on_delete=models.CASCADE, related_name='segregationbars_to')
    segregationlevel = models.SmallIntegerField(default=0)
    activate = models.BooleanField(default=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['fromclass', 'toclass'], name='unique_from_to_class'
            )
        ]
        db_table = 'goods.segregationbar'