from django.db import models


# Create your models here.
class ReadWise(models.Model):
    titulo = models.CharField(max_length=255, null=False, blank=False)
    autor = models.CharField(max_length=255, null=False, blank=False)
    data_lancamento = models.DateTimeField(auto_now_add=True, null=False, blank=False)
