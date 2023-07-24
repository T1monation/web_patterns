from django.db import models
from mainapp.models import Phone


class Repair(models.Model):
    phone = models.ForeignKey(Phone, on_delete=models.CASCADE,
                              verbose_name='Смартфон')
    STATUSES = (
        ('N', 'NO'),
        ('P', 'PROCESS'),
        ('D', 'DONE')
    )
    status = models.CharField(max_length=1,
                              choices=STATUSES,
                              verbose_name='статус')
    create = models.DateTimeField(auto_now_add=True,
                                  verbose_name='дата и время создания')
