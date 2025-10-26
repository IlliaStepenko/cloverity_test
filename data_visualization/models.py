from django.db import models


class RegionBase(models.Model):
    name = models.CharField(max_length=500)

    class Meta:
        abstract = True

    def __str__(self):
        return "{}".format(self.name)


class Region(RegionBase):
    class Meta:
        db_table = 'regions'


class SubRegion(Region):
    class Meta:
        db_table = 'sub_regions'


class DataItem(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='region_statistic')
    sub_region = models.ForeignKey(SubRegion, on_delete=models.CASCADE, related_name='sub_region_statistic')
    value = models.IntegerField(default=0)

    class Meta:
        db_table = 'data_items'

    def __str__(self):
        return "{} - {} - {}".format(self.region.name, self.sub_region.name, self.value)
