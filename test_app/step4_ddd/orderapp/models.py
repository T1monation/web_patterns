from django.db import models
from django.contrib.auth.models import User


class Phone(models.Model):
    name = models.CharField(max_length=32,
                            unique=True,
                            verbose_name='название')
    cost = models.DecimalField(max_digits=11,
                               decimal_places=2,
                               verbose_name='цена')


class Order(models.Model):
    user = models.ForeignKey(User,
                             verbose_name='покупатель',
                             on_delete=models.PROTECT)


class OrderItem(models.Model):
    phone = models.ForeignKey(Phone,
                              on_delete=models.PROTECT,
                              verbose_name='смартфон')
    count = models.PositiveSmallIntegerField(verbose_name='количество')
    order = models.ForeignKey(Order,
                              on_delete=models.PROTECT,
                              verbose_name='заказ')
