from django.db import models

#base model emiten
class Emiten(models.Model):
    emiten_code = models.TextField(db_column='emiten_code', blank=True, null=True)  # Field name made lowercase.
    emiten_name = models.TextField(db_column='emiten_name', blank=True, null=True)  # Field name made lowercase.
    class Meta:
        db_table = 'emiten'
        ordering = ['emiten_code']
    def __unicode__(self):
        return self.emiten_code
    def __str__(self):
        #return "%s %s" % (self.emiten_code, self.emiten_name)
        return self.emiten_code

#base model tbp_table2
class TbpTable2(models.Model):
    title = models.TextField(db_column='title', blank=True, null=True)
    source = models.TextField(db_column='source', blank=True, null=True)
    date = models.DateField(db_column='date', blank=True, null=True)
    paragraph = models.TextField(db_column='paragraph', blank=True, null=True)
    emiten = models.ForeignKey(Emiten, on_delete=models.PROTECT, blank=True, null=True)
    class Meta:
        db_table = 'tbp_table2'
    def __unicode__(self):
        return self.title





